
#include <ErrorHandler/qt_rule_engine.h>

#include <boost/bind.hpp>
#include <QtCore/QMetaType>

using namespace novadaq::errorhandler;

qt_rule_engine::qt_rule_engine( fhicl::ParameterSet const & pset
                              , QObject * parent )
: QObject( parent )
, engine ( pset
         , boost::bind(&qt_rule_engine::new_alarm, this, _1, _2) 
         , boost::bind(&qt_rule_engine::cond_match, this, _1) )
{

}

qt_rule_engine::~qt_rule_engine()
{

}

void qt_rule_engine::new_alarm( string_t const & rule_name
                              , string_t const & msg )
{ 
  emit alarm( QString(rule_name.c_str()), QString(msg.c_str()) ); 
}

void qt_rule_engine::cond_match( string_t const & cond_name )
{ 
  emit match( QString(cond_name.c_str()) ); 
}

QVector<QString> 
  qt_rule_engine::cond_names() const
{
  QVector<QString> names;
  strings_t::const_iterator it = engine.cond_names().begin();
  for( ; it!=engine.cond_names().end(); ++it)
    names.push_back( QString(it->c_str()) );
  return names;
}

QVector<QString> 
  qt_rule_engine::rule_names() const
{
  QVector<QString> names;
  strings_t::const_iterator it = engine.rule_names().begin();
  for( ; it!=engine.rule_names().end(); ++it)
    names.push_back( QString(it->c_str()) );
  return names;
}

QVector<QString>
  qt_rule_engine::rule_cond_names( QString const & name ) const
{
  strings_t const & std_names = engine.rule_cond_names( name.toUtf8().constData() );

  QVector<QString> names;

  strings_t::const_iterator it = std_names.begin();
  for( ; it!=std_names.end(); ++it)
    names.push_back( QString(it->c_str()) );
  return names;
}












