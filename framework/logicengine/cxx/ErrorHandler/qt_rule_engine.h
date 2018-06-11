#ifndef ERROR_HANDLER_QT_RULE_ENGINE_H
#define ERROR_HANDLER_QT_RULE_ENGINE_H


#include <ErrorHandler/ma_rule_engine.h>

#include <QtCore/QObject>
#include <QtCore/QVector>

namespace fhicl
{
  class ParameterSet;
}

namespace novadaq {
namespace errorhandler {


class qt_rule_engine : public QObject
{
  Q_OBJECT

public:

  // c'tor
  qt_rule_engine( fhicl::ParameterSet const & pset
                , QObject *parent = 0 );

  // d'tor
  ~qt_rule_engine();

  // rule_engine accessor
  size_t cond_size() const { return engine.cond_size(); }
  size_t rule_size() const { return engine.rule_size(); }

  QVector<QString> cond_names() const;
  QVector<QString> rule_names() const;

  bool is_EHS() const { return engine.is_EHS(); }

  // raw configuration
  fhicl::ParameterSet get_configuration() const
    { return engine.get_configuration(); }

  // condition fields
  QString cond_description( QString const & name ) const
    { return QString(engine.cond_description(name.toUtf8().constData()).c_str()); }

  QString cond_sources    ( QString const & name ) const 
    { return QString(engine.cond_sources(name.toUtf8().constData()).c_str()); }

  QString cond_regex      ( QString const & name ) const 
    { return QString(engine.cond_regex(name.toUtf8().constData()).c_str()); }

  int     cond_msg_count  ( QString const & name ) const
    { return engine.cond_msg_count(name.toUtf8().constData()); }

  // rule fields
  QString rule_description( QString const & name ) const
    { return QString(engine.rule_description(name.toUtf8().constData()).c_str()); }

  QString rule_expr       ( QString const & name ) const 
    { return QString(engine.rule_expr(name.toUtf8().constData()).c_str()); }

  int     rule_alarm_count( QString const & name ) const
    { return engine.rule_alarm_count(name.toUtf8().constData()); }

  // name list of conditions associated with a rule
  QVector<QString> rule_cond_names ( QString const & name ) const;

  // enable/disable the rule with given name
  void enable_rule( QString const & name, bool flag )
    { engine.enable_rule(name.toUtf8().constData(), flag); }

  // enable/disable action
  void enable_EHS( bool flag )
    { engine.enable_EHS(flag); }

  // reset named rule
  void reset_rule( QString const & name )
    { engine.reset_rule(name.toUtf8().constData()); }

  // reset all rules
  void reset_rules( )
    { engine.reset_rules(); }

  // reset named cond
  void reset_cond( QString const & name )
    { engine.reset_cond(name.toUtf8().constData()); }

  // reset all conds
  void reset_conds( )
    { engine.reset_conds(); }

  // reset everything
  void reset( )
    { engine.reset(); }

  // participants
  void add_participant_group( string_t const & group )
    { engine.add_participant_group( group ); }

  void add_participant_group( string_t const & group, size_t size )
    { engine.add_participant_group( group, size ); }

  void add_participant      ( string_t const & group, string_t const & app )
    { engine.add_participant( group, app ); }

  void add_participant      ( string_t const & app )
    { engine.add_participant( app ); }

  size_t get_group_participant_count( string_t const & group ) const
    { return engine.get_group_participant_count(group); }

  size_t get_participant_count( ) const
    { return engine.get_participant_count(); }


public slots:

  // receiving a new message
  void feed( mf::MessageFacilityMsg const & msg ) { engine.feed(msg); }

signals:

  // emits when alarms triggered
  void alarm( QString const & /*rule name*/
            , QString const & /*message body*/);

  void match( QString const & );

private:

  void new_alarm ( string_t const & rule_name, string_t const & msg );
  void cond_match( string_t const & cond_name );

private:

  ma_rule_engine engine;

};


} // end of errorhandler
} // end of novadaq


#endif
