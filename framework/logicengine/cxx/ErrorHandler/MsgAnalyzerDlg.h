#ifndef _NOVA_MSG_ANALYZER_DLG_H_
#define _NOVA_MSG_ANALYZER_DLG_H_

#include "ui_MsgAnalyzerDlg.h"

#include <ErrorHandler/ma_utils.h>
#include <ErrorHandler/NodeInfo.h>
#include <ErrorHandler/qt_rule_engine.h>
#include <ErrorHandler/qt_log_reader.h>
#include <ErrorHandler/ma_rcclient.h>

#include <QtCore/QMutex>
#include <QtCore/QSignalMapper>
#include <QtGui/QMenu>

#include <boost/regex.hpp>
#include <boost/shared_ptr.hpp>

#include <map>
#include <list>
#include <string>

namespace novadaq {
namespace errorhandler {

typedef boost::regex                          regex_t;
typedef std::vector<regex_t>                  vregex_t;

typedef std::map<std::string, NodeInfo * >    map_t;

enum display_field_t { DESCRIPTION, EXPRESSION };

class MsgAnalyzerDlg : public QDialog, private Ui::MsgAnalyzerDlg
{
  Q_OBJECT
	
public:
  MsgAnalyzerDlg( std::string const & cfgfile, int p
                , QDialog *parent = 0 );

protected:
  virtual void closeEvent(QCloseEvent *event);

private slots:

  void onLoad();

  void onNewMsg(mf::MessageFacilityMsg const & mfmsg);
  void onNewSysMsg(mf::QtDDSReceiver::SysMsgCode, QString const & msg);

  void onNewAlarm( QString const & rule_name
                 , QString const & msg );
  void onConditionMatch( QString const & name );

  void reset();
  void exit();

  void onNodeClicked(QListWidgetItem * item);

  void show_main_context_menu(const QPoint & pos);
  void show_dcm_context_menu(const QPoint & pos);
  void show_evb_context_menu(const QPoint & pos);

  void context_menu_reset();
  void context_menu_warning();
  void context_menu_error();

  void open_log();
  void read_log();
  void read_completed();

  void rule_enable( );
  void rule_disable( );
  void rule_reset_selection( );
  void reset_rule(int idx);
  void reset_rule(QString);


  void onRuleDesc( bool checked ) 
    { rule_display = checked ? DESCRIPTION : EXPRESSION; updateRuleDisplay(); }
  void onCondDesc( bool checked )
    { cond_display = checked ? DESCRIPTION : EXPRESSION; updateCondDisplay(); }

  void onEstablishPartition(int partition);
  void onSetParticipants( QVector<QString> const & dcm
                        , QVector<QString> const & bnevb);

private:

  void reset_node_status();
  void reset_rule_engine();

  void initNodeStatus();
  void initParticipants();
  void initRuleEngineTable();
  void updateRuleDisplay();
  void updateCondDisplay();

  void publishMessage( message_type_t type, QString const & msg ) const;

  void show_context_menu( QPoint const & pos, QListWidget * list );
  bool check_node_aow( std::string const & key );
  bool check_node_aoe( std::string const & key );

private:

  // data member
  fhicl::ParameterSet    pset;
  mf::QtDDSReceiver      qtdds;
  qt_rule_engine         engine;
  qt_log_reader          reader;

  novadaq::rcclient::ma_rcclient 
                         rcclient;

  map_t                  map;
  int                    nmsgs;

  // number of rules/conditions
  size_t                 rule_size;
  size_t                 cond_size;

  // rule/cond name --> row index map
  std::map<QString, int> rule_idx_map;
  std::map<QString, int> cond_idx_map;

  // whether to show description or expression
  display_field_t        rule_display;
  display_field_t        cond_display;

  // map lock
  QMutex                 map_lock;

  // signal mapper
  QSignalMapper          sig_mapper;

  // conext menu
  QMenu                * context_menu;
  QMenu                * rule_act_menu;
  QMenu                * cond_act_menu;

  // context menu actions
  QAction              * act_reset;
  QAction              * act_warning;
  QAction              * act_error;
  QAction              * act_rule_enable;
  QAction              * act_rule_disable;
  QAction              * act_rule_reset;

  // QListWidgetItem related to the context menu
  QListWidgetItem      * list_item;

  // Node Status related members
  bool                   aow_any;  // alarm on warning on any nodes
  bool                   aoe_any;  // alarm on error on any nodes
  vregex_t               e_aow;    // regex expressions for aow
  vregex_t               e_aoe;    // regex expressions for aoe
  boost::smatch          what_;

};
    
} // end of namespace errorhandler
} // end of namespace novadaq

#endif
