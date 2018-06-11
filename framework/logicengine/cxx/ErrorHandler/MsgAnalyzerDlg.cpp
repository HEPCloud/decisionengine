
#include <ErrorHandler/MsgAnalyzerDlg.h>
#include <ErrorHandler/MsgBox.h>
#include <ErrorHandler/ma_participants.h>

#include <cetlib/filepath_maker.h>
#include <fhiclcpp/make_ParameterSet.h>

#include <QtCore/QDateTime>
#include <QtCore/QSettings>
#include <QtCore/QTimer>

#include <QtGui/QMessageBox>
#include <QtGui/QFileDialog>
#include <QtGui/QMenu>

#include <memory>

using fhicl::ParameterSet;
using namespace novadaq::errorhandler;

static ParameterSet 
  read_conf( string_t const fname )
{
  std::auto_ptr<cet::filepath_maker> policy;

  if( fname[0]=='/' ) policy.reset(new cet::filepath_maker());
  else                policy.reset(new cet::filepath_lookup("FHICL_FILE_PATH"));

  LOG_DEBUG("") << "message analyzer configuration file: " 
                << fname;

  ParameterSet pset;

  // it throws when the file is not parsable
  fhicl::make_ParameterSet( fname, *policy, pset );

  return pset;
}

MsgAnalyzerDlg::MsgAnalyzerDlg( std::string const & cfgfile, int partition
                              , QDialog * parent)
: pset(read_conf(cfgfile))
, qtdds("MessageAnalyzer", partition)
, engine(pset)
, rcclient("MessageAnalyzer", partition)
, map()
, nmsgs(0)
, rule_size(0)
, cond_size(0)
, rule_idx_map()
, cond_idx_map()
, rule_display( DESCRIPTION )
, cond_display( DESCRIPTION )
, map_lock()
, sig_mapper(this)
, context_menu( new QMenu(this) )
, rule_act_menu( new QMenu(this) )
, cond_act_menu( new QMenu(this) )
, list_item(NULL)
, aow_any(false)
, aoe_any(false)
, e_aow()
, e_aoe()
{
  setupUi(this);
  this->setWindowTitle("NOvA Message Analyzer, Partition " + QString::number(partition));

  connect( &qtdds , SIGNAL(newMessage(mf::MessageFacilityMsg const & ))
         , this   , SLOT(onNewMsg(mf::MessageFacilityMsg const & )) );

  connect( &qtdds , SIGNAL(newMessage(mf::MessageFacilityMsg const & ))
         , &engine, SLOT(feed(mf::MessageFacilityMsg const & )) );

  connect( &engine, SIGNAL(alarm(QString const &, QString const &))
         , this   , SLOT(onNewAlarm(QString const &, QString const &)) );

  connect( &engine, SIGNAL(match(QString const &))
         , this   , SLOT(onConditionMatch(QString const &)) );

  connect( &rcclient, SIGNAL(establishPartition(int))
         , this     , SLOT(onEstablishPartition(int)) );

  connect( &rcclient, SIGNAL(setParticipants(QVector<QString> const &, QVector<QString> const &))
         , this     , SLOT(onSetParticipants(QVector<QString> const &, QVector<QString> const &)) );

#if 0
  connect( &qtdds
         , SIGNAL(newSysMessage(mf::QtDDSReceiver::SysMsgCode, QString const & ))
         , this
         , SLOT(onNewSysMsg(mf::QtDDSReceiver::SysMsgCode, QString const & )) );
#endif

  connect( btnReset, SIGNAL( clicked() ), this, SLOT( reset() ) );
  connect( btnExit , SIGNAL( clicked() ), this, SLOT( exit()  ) );

  connect( btnOpenLog, SIGNAL( clicked() ), this, SLOT( open_log() ) );
  connect( btnReadLog, SIGNAL( clicked() ), this, SLOT( read_log() ) );

  connect( &reader, SIGNAL( updateProgress(int) ), pbLog, SLOT( setValue(int) ) );
  connect( &reader, SIGNAL( readCompleted (   ) ), this , SLOT( read_completed() ) );

  connect( lwMain  , SIGNAL( itemDoubleClicked(QListWidgetItem *) )
         , this    , SLOT  ( onNodeClicked(QListWidgetItem *) ) );
  connect( lwDCM   , SIGNAL( itemDoubleClicked(QListWidgetItem *) )
         , this    , SLOT  ( onNodeClicked(QListWidgetItem *) ) );
  connect( lwBN    , SIGNAL( itemDoubleClicked(QListWidgetItem *) )
         , this    , SLOT  ( onNodeClicked(QListWidgetItem *) ) );

  connect( rbRuleDesc, SIGNAL(toggled(bool)), this, SLOT(onRuleDesc(bool)) );
  connect( rbCondDesc, SIGNAL(toggled(bool)), this, SLOT(onCondDesc(bool)) );

  connect( &sig_mapper, SIGNAL(mapped(int)) , this, SLOT(reset_rule(int)) );
  connect( &sig_mapper, SIGNAL(mapped(QString)) , this, SLOT(reset_rule(QString)) );



  // node status panel context menu
  connect( lwDCM , SIGNAL( customContextMenuRequested(const QPoint&) )
         , this  , SLOT  ( show_dcm_context_menu(const QPoint&) ) );
  connect( lwBN  , SIGNAL( customContextMenuRequested(const QPoint&) )
         , this  , SLOT  ( show_evb_context_menu(const QPoint&) ) );
  connect( lwMain, SIGNAL( customContextMenuRequested(const QPoint&) )
         , this  , SLOT  ( show_main_context_menu(const QPoint&) ) );

  act_reset = new QAction("Reset", 0);
  context_menu->addAction(act_reset);

  context_menu->addSeparator();

  act_warning = new QAction("Alarm on warning", 0);
  act_warning->setCheckable(true);
  context_menu->addAction(act_warning);

  act_error = new QAction("Alarm on error", 0);
  act_error->setCheckable(true);
  context_menu->addAction(act_error);

  // context menu action trigger
  connect( act_reset  , SIGNAL( triggered() ), this, SLOT( context_menu_reset() ) );
  connect( act_warning, SIGNAL( triggered() ), this, SLOT( context_menu_warning() ) );
  connect( act_error  , SIGNAL( triggered() ), this, SLOT( context_menu_error() ) );

  // rule action menu
  act_rule_enable = new QAction("Enable selections", 0);
  act_rule_disable = new QAction("Disable selections", 0);
  act_rule_reset = new QAction("Reset selections", 0);

  rule_act_menu->addAction(act_rule_enable);
  rule_act_menu->addAction(act_rule_disable);
  rule_act_menu->addSeparator();
  rule_act_menu->addAction(act_rule_reset);

  btnRuleAct->setMenu(rule_act_menu);

  // rule action menu trigger
  connect( act_rule_enable , SIGNAL( triggered() ), this, SLOT( rule_enable() ) );
  connect( act_rule_disable, SIGNAL( triggered() ), this, SLOT( rule_disable() ) );
  connect( act_rule_reset  , SIGNAL( triggered() ), this, SLOT( rule_reset_selection() ) );

  // Node Status configuration
  initNodeStatus( );

  // init rule engine tables 
  initRuleEngineTable();
  initParticipants();

  // system message
  QString msg("Loaded rule engine configuration from '");
  msg.append(cfgfile.c_str()).append("'");
  publishMessage( MSG_SYSTEM, msg );

  // handshake
#if 0
  if( engine.is_EHS() )
  {
    qtdds.setHandshakeResponse("0");
    QVector<QString> res = qtdds.handshake();

    for(int i=0; i<res.size(); ++i)
      publishMessage( MSG_SYSTEM, res[i] );

    qtdds.setHandshakeResponse("1");
  }
#endif

  // conclude
  publishMessage( MSG_SYSTEM, "Rule engine initialization completed.");
 
  pbLog->setMaximum(100);
  pbLog->setMinimum(0);
  pbLog->setValue(0);

  btnReadLog->setEnabled(false);

  QTimer::singleShot(100, this, SLOT( onLoad() ) );
}

void MsgAnalyzerDlg::onLoad()
{
  if( engine.is_EHS() )
  {
    publishMessage( MSG_SYSTEM, "Looking for active Error Handling Supervisor" );

    // "-1" means unknown
    qtdds.setHandshakeResponse("-1");

    int retries = 0;
    bool hs_success = false;

    do
    {
      QVector<QString> res = qtdds.handshake();

      int unknown = 0;
      int active = 0;

      for(int i=0; i<res.size(); ++i)
      {
        if( res[i]=="-1" )
          ++unknown;
        else if( res[i]=="1" )
          ++active;
      }

      if( unknown>1 ) 
      {
        // someone else is also querying for EHS
        ++retries;
        hs_success = false;
        sleep(3);
      }
      else if( active==0 )
      {
        // i now have the control
        publishMessage( MSG_SYSTEM
                      , tr("None EHS has been found. "
                           "Current instance of the Message Analyzer "
                           "will act as an EHS") );
        qtdds.setHandshakeResponse("1");
        hs_success = true;
      }
      else
      {
        // someone else has the control
        QString s = QString("Found ") + QString::number(active) + " active EHS!";
        publishMessage( MSG_ERROR, s );

        int ret = QMessageBox::critical( this
                                       , tr("MessageAnalyzer")
                                       , tr("Found one or more active Error Handler Supervisors running in the system."
                                            "Do you wish to disable the EHS?\n\n"
                                            "Click Yes to diable.\n"
                                            "CLick Close to exit the MessageAnalyzer\n"
                                            "Click Ignore to continue with EHS enabled(DANGEROUS)!")
                                       , QMessageBox::Close | QMessageBox::Yes | QMessageBox::Ignore
                                       , QMessageBox::Yes );

        if( ret==QMessageBox::Close )
        {
          qtdds.setHandshakeResponse("0");
          close();
        }

        if( ret==QMessageBox::Yes )
        {
          engine.enable_EHS( false );
          qtdds.setHandshakeResponse("0");
          publishMessage( MSG_SYSTEM
                        , "EHS has been disabled on this client." );
          hs_success = true;
        }
        else
        {

          s = QString("EHS remains enabled while there is(are) ")
              + QString::number(active)
              + QString(" active EHS in the sysmte!");
          publishMessage( MSG_WARNING, s );
          qtdds.setHandshakeResponse("1");
          hs_success = true;
        }
      }
    } while( !hs_success && retries<5 );

    if( hs_success==false )
    {
      QMessageBox::critical( this
                           , tr("MessageAnalyzer")
                           , tr("Handshaking failed! Click OK to close the application.")
                            , QMessageBox::Ok 
                            , QMessageBox::Ok );
      close();
    }
  }
}

void MsgAnalyzerDlg::initNodeStatus( )
{
  ParameterSet null_pset;
  ParameterSet node = pset.get<ParameterSet>("node_status", null_pset);

  typedef std::string              string_t;
  typedef std::vector<std::string> strings_t;

  strings_t null_strings;

  strings_t aow = node.get<strings_t>("alarm_on_first_warning", null_strings);
  strings_t aoe = node.get<strings_t>("alarm_on_first_error", null_strings);

  for(size_t i=0; i<aow.size(); ++i)
  {
    if( aow[i]=="*" )
    {
      aow_any = true;
      break;
    }

    e_aow.push_back(regex_t(aow[i]));
  }

  for(size_t i=0; i<aoe.size(); ++i)
  {
    if( aoe[i] == "*" )
    {
      aoe_any = true;
      break;
    }

    e_aoe.push_back(regex_t(aoe[i]));
  }
}

bool MsgAnalyzerDlg::check_node_aow( std::string const & key )
{
  if( aow_any ) return true;

  for(size_t i=0; i<e_aow.size(); ++i)
  {
    if( boost::regex_match(key, what_, e_aow[i]) ) return true;
  }

  return false;
}

bool MsgAnalyzerDlg::check_node_aoe( std::string const & key )
{
  if( aoe_any ) return true;

  for(size_t i=0; i<e_aoe.size(); ++i)
  {
    if( boost::regex_match(key, what_, e_aoe[i]) ) return true;
  }

  return false;
}

void MsgAnalyzerDlg::onNewMsg(mf::MessageFacilityMsg const & mfmsg)
{
  // basic message filtering according to the host and app
  std::string  key;
  node_type_t type = get_source_from_msg(key, mfmsg);

  QListWidget *lw;
  if (type==DCM)             lw = lwDCM;
  else if (type==BufferNode) lw = lwBN;
  else                       lw = lwMain;

  node_status status = NORMAL;

  map_lock.lock();
  {
    map_t::iterator it = map.find(key);

    if (it==map.end())  // first msg from the key
    {
      bool aow = check_node_aow(key);
      bool aoe = check_node_aoe(key);

      NodeInfo * ni = new NodeInfo(type, key, lw, aow, aoe);
      status = ni->push_msg(mfmsg);
      map.insert(std::make_pair(key, ni));
    }
    else // found existing key
    {
      status = it->second->push_msg(mfmsg);
    }

    ++nmsgs;
    lcdMsgs->display(nmsgs);
  }
  map_lock.unlock();

  if( status==FIRST_WARNING )
  {
    QString str = QString(key.c_str())
                  .append(" has issued a warning message:\n")
                  .append(mfmsg.message().c_str());                    
    publishMessage(MSG_WARNING, str); 
  }
  else if( status==FIRST_ERROR )
  {
    QString str = QString(key.c_str())
                  .append(" has issued an error message:\n")
                  .append(mfmsg.message().c_str());                    
    publishMessage(MSG_ERROR, str); 
  }

}

void 
  MsgAnalyzerDlg::publishMessage( message_type_t type
                                , QString const & msg ) const
{
  QString txt;

  txt.append(QDateTime::currentDateTime().toString("[MM/dd/yyyy h:m:ss ap] "));
  txt.append(get_message_type_str(type).c_str())
     .append(":\n")
     .append(msg)
     .append("\n");

  QListWidgetItem * lwi = new QListWidgetItem(txt);

  switch(type)
  {
  case MSG_SYSTEM:  lwi->setForeground(QBrush(Qt::blue));    break;
  case MSG_ERROR:   lwi->setForeground(QBrush(Qt::red));     break;
  case MSG_WARNING: lwi->setForeground(QBrush(Qt::magenta)); break;
  default:          lwi->setForeground(QBrush(Qt::darkGreen));
  }

  lwAlerts->insertItem(0, lwi);
}


void MsgAnalyzerDlg::onNewAlarm( QString const & rule_name
                               , QString const & msg )
{
  publishMessage( MSG_ERROR, msg );

  std::map<QString,int>::const_iterator it = rule_idx_map.find(rule_name);

  if( it==rule_idx_map.end() )
    throw std::runtime_error(  "MsgAnalyzerDlg::onNewAlarm() rule name '"
                             + std::string(rule_name.toUtf8().constData())
                             + "' not found");

  int alarms = engine.rule_alarm_count(it->first);
  twRules->item(it->second, 2)->setText(QString("x ").append(QString::number(alarms)));

  QBrush brush(QColor(255,200,200));

  twRules->item(it->second, 0)->setBackground(brush);
  twRules->item(it->second, 1)->setBackground(brush);
  twRules->item(it->second, 2)->setBackground(brush);

  QPushButton * btn = new QPushButton("Rst");
  btn->setFixedSize(62,20);
  
  twRules->setCellWidget(it->second, 3, btn);

  sig_mapper.setMapping(btn, it->second);
  connect(btn, SIGNAL(clicked()), &sig_mapper, SLOT(map()));
}

void MsgAnalyzerDlg::onConditionMatch( QString const & cond_name )
{
  std::map<QString,int>::const_iterator it = cond_idx_map.find(cond_name);

  if( it==cond_idx_map.end() )
    throw std::runtime_error(  "MsgAnalyzerDlg::onConditionMatch() name '"
                             + std::string(cond_name.toUtf8().constData())
                             + "' not found");

  int msg_count = engine.cond_msg_count(cond_name);
  twConds->item(it->second, 3)->setText(QString::number(msg_count));

  if( msg_count==1 )
  {
    // paint blue when first message captured
    QBrush brush(QColor(230,230,255));
    twConds->item(it->second, 0)->setBackground(brush);
    twConds->item(it->second, 1)->setBackground(brush);
    twConds->item(it->second, 2)->setBackground(brush);
    twConds->item(it->second, 3)->setBackground(brush);
  }

}


void MsgAnalyzerDlg::onNewSysMsg(mf::QtDDSReceiver::SysMsgCode, QString const & msg)
{

}

void MsgAnalyzerDlg::show_dcm_context_menu(QPoint const & pos)
{
  show_context_menu(pos, lwDCM);
}

void MsgAnalyzerDlg::show_evb_context_menu(QPoint const & pos)
{
  show_context_menu(pos, lwBN);
}

void MsgAnalyzerDlg::show_main_context_menu(QPoint const & pos)
{
  show_context_menu(pos, lwMain);
}

void MsgAnalyzerDlg::show_context_menu(QPoint const & pos, QListWidget * list)
{
  list_item = list->itemAt(pos);

  if( list_item!=NULL )
  {
    QVariant v = list_item->data(Qt::UserRole);
    NodeInfo * ni = (NodeInfo *)v.value<void*>();

    act_warning->setChecked( ni->alarm_on_warning() );
    act_error->setChecked( ni->alarm_on_error() );

    context_menu->exec(QCursor::pos());
  }
}

void MsgAnalyzerDlg::context_menu_reset()
{
  QVariant v = list_item->data(Qt::UserRole);
  NodeInfo * ni = (NodeInfo *)v.value<void*>();

  ni->reset();
}

void MsgAnalyzerDlg::context_menu_warning()
{
  bool flag = act_warning->isChecked();

  QVariant v = list_item->data(Qt::UserRole);
  NodeInfo * ni = (NodeInfo *)v.value<void*>();
  
  ni->set_alarm_on_warning(flag);
}

void MsgAnalyzerDlg::context_menu_error()
{
  bool flag = act_error->isChecked();

  QVariant v = list_item->data(Qt::UserRole);
  NodeInfo * ni = (NodeInfo *)v.value<void*>();
  
  ni->set_alarm_on_error(flag);
}

void MsgAnalyzerDlg::onEstablishPartition(int partition)
{
  reset_node_status();
  reset_rule_engine();

  publishMessage( MSG_SYSTEM, "Message Analyzer has been reset" );
  publishMessage( MSG_SYSTEM, "Partition established." );
}

void MsgAnalyzerDlg::reset_node_status()
{
  map_lock.lock();
  {
    for(int i=lwMain->count(); i>0; --i)
      delete lwMain->takeItem(i-1);

    for(int i=lwBN->count();   i>0; --i)
      delete lwBN->takeItem(i-1);

    for(int i=lwDCM->count();  i>0; --i)
      delete lwDCM->takeItem(i-1);

    for(map_t::iterator it=map.begin() ; it!=map.end(); ++it)
      delete it->second;

    map.clear();

    nmsgs = 0;
    lcdMsgs->display(nmsgs);
  }
  map_lock.unlock();
}

void MsgAnalyzerDlg::reset_rule_engine()
{
  std::map<QString,int>::const_iterator it;

  // reset conds
  for( it=cond_idx_map.begin(); it!=cond_idx_map.end(); ++it )
  {
    twConds->item(it->second, 3)->setText("0");

    QBrush brush(QColor(255,255,255));
    twConds->item(it->second, 0)->setBackground(brush);
    twConds->item(it->second, 1)->setBackground(brush);
    twConds->item(it->second, 2)->setBackground(brush);
    twConds->item(it->second, 3)->setBackground(brush);
  }

  // reset rules
  for( it=rule_idx_map.begin(); it!=rule_idx_map.end(); ++it )
  {
    twRules->item(it->second, 2)->setText("");

    QBrush brush(QColor(255,255,255));
    twRules->item(it->second, 0)->setBackground(brush);
    twRules->item(it->second, 1)->setBackground(brush);
    twRules->item(it->second, 2)->setBackground(brush);

    QWidget * temp = new QWidget();
    twRules->setCellWidget(it->second, 3, temp);
  }

  // reset engine
  engine.reset();
}

void MsgAnalyzerDlg::reset()
{
  int ret = QMessageBox::warning(this
               , "MsgAnalyzer"
               , "Are you sure you erase all messages and reset the MsgAnalyzer?"
               , QMessageBox::Cancel | QMessageBox::Ok
               , QMessageBox::Cancel );

  if (ret == QMessageBox::Cancel) return;

  reset_node_status();
  reset_rule_engine();

  publishMessage(MSG_SYSTEM, "Message Analyzer has been reset");
}

void MsgAnalyzerDlg::exit()
{
  int ret = QMessageBox::warning(this
         , "MsgAnalyzer"
         , "Are you sure you wish to close MsgAnalyzer? This is usually not the correct procedure!"
         , QMessageBox::Cancel | QMessageBox::Ok
         , QMessageBox::Cancel );

  if (ret == QMessageBox::Cancel) return;

  close();
}

void MsgAnalyzerDlg::closeEvent(QCloseEvent *event)
{
  QSettings settings("NOvA DAQ", "MsgAnalyzer");
  settings.setValue("geometry", saveGeometry());
  QDialog::closeEvent(event);
}

void MsgAnalyzerDlg::rule_enable()
{
  std::map<QString, int>::const_iterator it = rule_idx_map.begin();
  for( ; it!=rule_idx_map.end(); ++it)
  {
    if(twRules->item(it->second, 0)->checkState() == Qt::Checked )
    {
      // enable rule
      engine.enable_rule(it->first, true);

      // uncheck selection
      twRules->item(it->second, 0)->setCheckState(Qt::Unchecked);

      // paint foreground to black
      QBrush black(QColor(0,0,0));
      twRules->item(it->second, 0)->setForeground(black);
      twRules->item(it->second, 1)->setForeground(black);
      twRules->item(it->second, 2)->setForeground(black);
      twRules->cellWidget(it->second, 3)->setEnabled(true);

      int alarms = engine.rule_alarm_count(it->first);

      if( alarms==0 ) twRules->item(it->second, 2)->setText("");
      else            twRules->item(it->second, 2)->setText(QString("x ")
                                                    .append(QString::number(alarms)));
    }
  }
}

void MsgAnalyzerDlg::rule_disable()
{
  std::map<QString, int>::const_iterator it = rule_idx_map.begin();
  for( ; it!=rule_idx_map.end(); ++it)
  {
    if(twRules->item(it->second, 0)->checkState() == Qt::Checked )
    {
      // disable rule
      engine.enable_rule(it->first, false);

      // uncheck selection
      twRules->item(it->second, 0)->setCheckState(Qt::Unchecked);

      // paint foreground to grey
      twRules->item(it->second, 2)->setText("Disabled");

      QBrush brush(QColor(200,200,200));
      twRules->item(it->second, 0)->setForeground(brush);
      twRules->item(it->second, 1)->setForeground(brush);
      twRules->item(it->second, 2)->setForeground(brush);
      twRules->cellWidget(it->second, 3)->setEnabled(false);
    }
  }

}

void MsgAnalyzerDlg::rule_reset_selection( )
{
  std::map<QString, int>::const_iterator it = rule_idx_map.begin();
  for( ; it!=rule_idx_map.end(); ++it)
  {
    if(twRules->item(it->second, 0)->checkState() == Qt::Checked )
    {
      // reset rule
      reset_rule(it->second);

      // uncheck selection
      twRules->item(it->second, 0)->setCheckState(Qt::Unchecked);
    }
  }
}


// make one that works with a QString 
void MsgAnalyzerDlg::reset_rule(QString name)
{
  std::map<QString, int>::const_iterator it = rule_idx_map.find(name);
  this->reset_rule(it->second);

  twRules->item(it->second, 0)->setCheckState(Qt::Unchecked);
  return;
}


// called by individual reset button of rules
// currently not in use
void MsgAnalyzerDlg::reset_rule(int idx)
{
  QString rule_name = twRules->item(idx, 0)->text();

  engine.reset_rule(rule_name);

  // paint background
  QBrush brush(QColor(255,255,255));
  twRules->item(idx, 0)->setBackground(brush);
  twRules->item(idx, 1)->setBackground(brush);
  twRules->item(idx, 2)->setBackground(brush);

  // status column
  twRules->item(idx, 2)->setText("");

  // remove reset button
  QWidget * temp = new QWidget();
  twRules->setCellWidget(idx, 3, temp);

  // repaint affected conditions
  QVector<QString> cond_names = engine.rule_cond_names(rule_name);
  for(int i=0; i<cond_names.size(); ++i)
  {
    std::map<QString, int>::const_iterator it = cond_idx_map.find(cond_names[i]);

    if( it!=cond_idx_map.end() )
    {
      QBrush brush(QColor(255,255,255));
      twConds->item(it->second, 0)->setBackground(brush);
      twConds->item(it->second, 1)->setBackground(brush);
      twConds->item(it->second, 2)->setBackground(brush);
      twConds->item(it->second, 3)->setBackground(brush);
      
      twConds->item(it->second, 3)->setText("0");
    }
  }

  publishMessage( MSG_SYSTEM, "reset rule " + twRules->item(idx,0)->text() );
}

void MsgAnalyzerDlg::onNodeClicked(QListWidgetItem * item)
{
  QVariant v = item->data(Qt::UserRole);
  NodeInfo * ni = (NodeInfo *)v.value<void*>();

  MsgBox msgbox(QString(ni->key_string().c_str()), *ni);
  msgbox.exec();
}

void MsgAnalyzerDlg::initRuleEngineTable()
{

  twRules->setColumnWidth(0, 100);
  twRules->setColumnWidth(1, 320);
  twRules->setColumnWidth(2, 70);
  twRules->setColumnWidth(3, 62);

  rule_size = engine.rule_size();
  twRules->setRowCount(rule_size);

  rbRuleDesc->setChecked(true);
  rbRuleExpr->setChecked(false);

  QVector<QString> rule_names = engine.rule_names();

  // reset button for each rule has been commented out
  for(size_t i=0; i<rule_size; ++i)
  {
    twRules->setRowHeight(i, 20);
    QString name = rule_names[i];
    QTableWidgetItem * iname = new QTableWidgetItem(name);
    QTableWidgetItem * iexpr = new QTableWidgetItem();
    QTableWidgetItem * istat = new QTableWidgetItem();
    QWidget          * itemp = new QWidget();

    iname->setCheckState(Qt::Unchecked);
    istat->setTextAlignment(Qt::AlignHCenter | Qt::AlignVCenter);

    twRules->setItem(i, 0, iname);
    twRules->setItem(i, 1, iexpr);
    twRules->setItem(i, 2, istat);
    twRules->setCellWidget(i, 3, itemp);

    rule_idx_map.insert(std::make_pair(name, i));
  }

  // display descriptions or expressions?
  updateRuleDisplay();

  twConds->setColumnWidth(0, 100);
  twConds->setColumnWidth(1, 90);
  twConds->setColumnWidth(2, 320);
  twConds->setColumnWidth(3, 42);

  cond_size = engine.cond_size();
  twConds->setRowCount(cond_size);

  rbCondDesc->setChecked(true);
  rbCondRegx->setChecked(false);

  QVector<QString> cond_names = engine.cond_names();

  for(size_t i=0; i<cond_size; ++i)
  {
    twConds->setRowHeight(i, 20);
    QString name = cond_names[i];
    QTableWidgetItem * iname  = new QTableWidgetItem(name);
    QTableWidgetItem * ifrom  = new QTableWidgetItem(engine.cond_sources(name));
    QTableWidgetItem * iregex = new QTableWidgetItem();
    QTableWidgetItem * icount = new QTableWidgetItem("0");

    iname->setCheckState(Qt::Unchecked);
    icount->setTextAlignment(Qt::AlignRight | Qt::AlignVCenter);

    twConds->setItem(i, 0, iname);
    twConds->setItem(i, 1, ifrom);
    twConds->setItem(i, 2, iregex);
    twConds->setItem(i, 3, icount); 

    cond_idx_map.insert(std::make_pair(name, i));
  }

  updateCondDisplay();

}

void MsgAnalyzerDlg::updateRuleDisplay()
{
  std::map<QString, int>::const_iterator it = rule_idx_map.begin();

  for( ; it!=rule_idx_map.end(); ++it)
  {
    QString txt = (rule_display==DESCRIPTION) 
                      ? engine.rule_description(it->first) 
                      : engine.rule_expr(it->first);

    twRules -> item(it->second, 1) -> setText(txt);
  }
}

void MsgAnalyzerDlg::updateCondDisplay()
{
  std::map<QString, int>::const_iterator it = cond_idx_map.begin();

  for( ; it!=cond_idx_map.end(); ++it)
  {
    QString txt = (cond_display==DESCRIPTION) 
                      ? engine.cond_description(it->first) 
                      : engine.cond_regex(it->first);

    twConds -> item(it->second, 2) -> setText(txt);
  }
}

void MsgAnalyzerDlg::initParticipants()
{
  ma_participants & p = ma_participants::instance();

  // remove existing participants
  p.reset();
 
  // hardcoded participants and groups :
  // p.add_group( group_name, # of participants )
  p.add_group( "dcm", 8 );
  p.add_group( "bn",  8 );
}

void MsgAnalyzerDlg::onSetParticipants( QVector<QString> const & dcm
                                      , QVector<QString> const & bnevb )
{
  ma_participants & p = ma_participants::instance();

  p.reset();

  p.add_group( "dcm", dcm.size() );
  p.add_group( "bnevb", bnevb.size() );

  publishMessage( MSG_SYSTEM, "Initialized participants with " 
                   + QString(dcm.size())   + "dcm(s) and " 
                   + QString(bnevb.size()) + "bnevb(s)" );
}

void MsgAnalyzerDlg::open_log()
{

  QString filename = 
      QFileDialog::getOpenFileName( this
                                  , tr("Open Archive") 
                                  , "/home/qlu"
                                  , tr("Log Files (*.log);;All Files(*.*)") );

  if( filename.isEmpty() )
    return;

  if( reader.open(filename) )
  {

    // disconnect from DDS receiver
    disconnect( &qtdds , SIGNAL(newMessage(mf::MessageFacilityMsg const & ))
              , this   , SLOT(onNewMsg(mf::MessageFacilityMsg const & )) );

    disconnect( &qtdds , SIGNAL(newMessage(mf::MessageFacilityMsg const & ))
              , &engine, SLOT(feed(mf::MessageFacilityMsg const & )) );

    // connect from log reader
    connect( &reader, SIGNAL(newMessage(mf::MessageFacilityMsg const & ))
           , this   , SLOT(onNewMsg(mf::MessageFacilityMsg const & )) );

    connect( &reader, SIGNAL(newMessage(mf::MessageFacilityMsg const & ))
           , &engine, SLOT(feed(mf::MessageFacilityMsg const & )) );

    // init
    publishMessage( MSG_SYSTEM, "Disconnected from MessageFacility receiver");
    publishMessage( MSG_SYSTEM, "Message Log Analysis: " + filename );

    labelLogFile->setText( filename );

    pbLog->setValue(0);
    btnReadLog->setText("Start");
    btnReadLog->setEnabled(true);
    btnOpenLog->setEnabled(true);
  }
}


void MsgAnalyzerDlg::read_log()
{
  if( btnReadLog->text() == "Pause" )
  {
    reader.pause_exec();
    btnReadLog->setText("Resume");
    btnOpenLog->setEnabled(true);
  }
  else
  {
    reader.start();
    btnReadLog->setText("Pause");
    btnOpenLog->setEnabled(false);
  }
}

void MsgAnalyzerDlg::read_completed()
{
  btnReadLog->setText("Start");
  btnReadLog->setEnabled(true);
  btnOpenLog->setEnabled(true);
}




