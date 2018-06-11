#include <ErrorHandler/NodeInfo.h>
#include <sstream>

#include <QtGui/QPainter>

using namespace novadaq::errorhandler;

NodeInfo::NodeInfo ( node_type_t type
                   , std::string const & key 
                   , QListWidget * parent
                   , bool aow
                   , bool aoe )
: msgs_ptr    (new msgs_t)
, highest_sev (mf::QtDDSReceiver::DEBUG)
, item_ptr    ()
, node_type   (type)
, key_str (key)
, alarm_warning(aow)
, alarm_error(aoe)
{ 
  QString cap = get_caption(key);

  // icon
  int icon_w = 0; int icon_h = 0;
  get_icon_geometry(icon_w, icon_h);

  QPixmap pm(icon_w, icon_h);
  QIcon icon(pm);

  // list widget item
  item_ptr = new QListWidgetItem(icon, cap, parent);

  // node size
  int node_w = 0; int node_h = 0;
  get_node_geometry(node_w, node_h);
  QSize sz(node_w, node_h);
  item_ptr->setSizeHint(sz);

  // user data
  QVariant v = qVariantFromValue( (void*)this );
  item_ptr->setData(Qt::UserRole, v);

  //item_ptr->setData(Qt::UserRole, QVariant(key.c_str()));
  //item_ptr->setData(Qt::UserRole, QVariant::fromValue<msgs_ptr_t>(msgs_ptr)); 
}

node_status NodeInfo::push_msg ( msg_t const & msg )
{
  sev_code_t sev = mf::QtDDSReceiver::getSeverityCode(msg.severity());

  node_status status = NORMAL;

  if (sev >= highest_sev) 
  {
    // push the message into the queue
    if (msgs_ptr->size() > MAX_QUEUE)  msgs_ptr->pop_front();
    msgs_ptr->push_back(msg);

    // update icon
    if (sev > highest_sev) 
    {
      if( sev==mf::QtDDSReceiver::WARNING && alarm_warning)   
        status = FIRST_WARNING;
      else if( sev==mf::QtDDSReceiver::ERROR && alarm_error) 
        status = FIRST_ERROR;

      update_icon(sev);
    }

    // update hightest severity lvl
    highest_sev = sev;
  }

  return status;
}

void NodeInfo::reset()
{
  highest_sev = mf::QtDDSReceiver::DEBUG;
  update_icon(highest_sev);
}

QString NodeInfo::msgs_to_string() const
{
  QString txt;

  msgs_t::const_iterator it = msgs_ptr->begin();
  while (it!=msgs_ptr->end())
  {
    txt += get_html_str_from_msg(*it);
    ++it;
  }
    
  return txt;
}

QString NodeInfo::get_html_str_from_msg(mf::MessageFacilityMsg const & msg) const
{
  mf::QtDDSReceiver::SeverityCode sevid = 
                 mf::QtDDSReceiver::getSeverityCode(msg.severity());

  std::ostringstream ss;

  ss << "<font ";

  if     (sevid==mf::QtDDSReceiver::ERROR)    ss << "color='#FF0000'>";
  else if(sevid==mf::QtDDSReceiver::WARNING)  ss << "color='#E08000'>";
  else if(sevid==mf::QtDDSReceiver::INFO)     ss << "color='#008000'>";
  else                                        ss << "color='#505050'>";

  ss << "<b>" << msg.severity() << " / " << msg.category() << "</b><br>";
  ss << msg.timestr()  << "<br>";
  ss << msg.hostname() << " (" << msg.hostaddr() << ")" << "<br>";
  ss << msg.process()  << " (" << msg.pid()      << ")" << "<br>";
  ss << msg.file()     << " (" << msg.line() << ")" << "<br>";
  ss << msg.application() << " / "
     << msg.module()      << " / "
     << msg.context()     << "<br>";
  ss << msg.message()     << "<br>";
  ss << "</font><br>";

  return QString(ss.str().c_str());

}

void NodeInfo::update_icon ( sev_code_t sev )
{
  int icon_w = 0; int icon_h = 0;
  get_icon_geometry(icon_w, icon_h);

  QPixmap pm(icon_w, icon_h);
  pm.fill(Qt::transparent);

  QColor background;

  switch(sev)
  {
  case mf::QtDDSReceiver::ERROR:   
    background = QColor(255,  0,  0, 255); break;

  case mf::QtDDSReceiver::WARNING: 
    background = QColor(224,128,  0, 255); break;

  case mf::QtDDSReceiver::INFO:    
    background = QColor(  0,128,  0, 255); break;

  case mf::QtDDSReceiver::DEBUG:   
    background = QColor( 80, 80, 80, 255); break;

  default:                         
    background = QColor(200,200,200);
  }

  QPainter painter(&pm);

  QRect rect(2, 2, icon_w-4, icon_h-4);
  painter.setPen(Qt::NoPen);
  painter.fillRect(rect, background);

  QPen pen(Qt::black);
  painter.setPen(pen);

  QBrush brush(Qt::yellow);
  
  if(alarm_warning)
  {
    int off = alarm_error ? 22 : 11;
    QBrush brush(Qt::yellow);
    painter.setBrush(brush);
    painter.drawEllipse(icon_w-off, icon_h-11, 10, 10);
  }

  if(alarm_error) 
  {
    QBrush brush(Qt::red);
    painter.setBrush(brush);
    painter.drawEllipse(icon_w-11, icon_h-11, 10, 10);
  }

  QIcon icon(pm);

  item_ptr->setIcon(icon);
}

void NodeInfo::get_icon_geometry ( int & icon_w
                                 , int & icon_h ) const
{ 
  switch(node_type)
  {
  case BufferNode:
    icon_w = BUFFERNODE_ICON_WIDTH;
    icon_h = BUFFERNODE_ICON_HEIGHT;
    break;
  case DCM:
    icon_w = DCM_ICON_WIDTH;
    icon_h = DCM_ICON_HEIGHT;
    break;
  case MainComponent:
  default:
    icon_w = MAINCOMPONENT_ICON_WIDTH;
    icon_h = MAINCOMPONENT_ICON_HEIGHT;
  }
}

void NodeInfo::get_node_geometry ( int & node_w
                                 , int & node_h ) const
{ 
  switch(node_type)
  {
  case BufferNode:
    node_w = BUFFERNODE_NODE_WIDTH;
    node_h = BUFFERNODE_NODE_HEIGHT;
    break;
  case DCM:
    node_w = DCM_NODE_WIDTH;
    node_h = DCM_NODE_HEIGHT;
    break;
  case MainComponent:
  default:
    node_w = MAINCOMPONENT_NODE_WIDTH;
    node_h = MAINCOMPONENT_NODE_HEIGHT;
  }
}


QString NodeInfo::get_caption ( std::string const & key ) const
{
  if (node_type==BufferNode)  return key.substr(18).c_str();
  if (node_type==DCM)         return key.substr(4 ).c_str();

  return key.c_str();
}

