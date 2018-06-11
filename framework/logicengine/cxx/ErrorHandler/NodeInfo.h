#ifndef _NOVA_ERROR_HANDLER_NODE_INFO_H_
#define _NOVA_ERROR_HANDLER_NODE_INFO_H_

#include <ErrorHandler/ma_utils.h>

#include <QtGui/QListWidget>

#include <map>
#include <list>

namespace novadaq {
namespace errorhandler {

enum node_status { NORMAL, FIRST_WARNING, FIRST_ERROR };

class NodeInfo
{
public:

  msgs_sp_t         msgs_ptr;      // shared_ptr to msg list
  sev_code_t        highest_sev;   // highest severity lvl
  QListWidgetItem * item_ptr;      // ptr to QListWidgetItem
  node_type_t       node_type;     // node type (dcm, bn, or others)

  NodeInfo ( node_type_t type
           , std::string const & key
           , QListWidget * parent
           , bool aow
           , bool aoe );

  node_status push_msg ( msg_t const & msg );
  QString msgs_to_string () const;

  std::string key_string() const { return key_str; }

  bool alarm_on_warning() const { return alarm_warning; }
  bool alarm_on_error() const { return alarm_error; }

  void set_alarm_on_warning(bool flag) { alarm_warning = flag; update_icon(highest_sev); }
  void set_alarm_on_error(bool flag) { alarm_error = flag; update_icon(highest_sev); }

  void reset();

private:

  QString get_caption  ( std::string const & key ) const;
  void    get_icon_geometry ( int & icon_w, int & icon_h ) const;
  void    get_node_geometry ( int & node_w, int & node_h ) const;
  QString get_html_str_from_msg ( msg_t const & msg ) const;
  void    update_icon  ( sev_code_t sev );

private:

  std::string key_str;

  bool alarm_warning;
  bool alarm_error;

private:

  static const size_t MAX_QUEUE = 10;

public:

  static const int MAINCOMPONENT_ICON_WIDTH  = 34;
  static const int MAINCOMPONENT_ICON_HEIGHT = 34;
  static const int MAINCOMPONENT_NODE_WIDTH  = 80;
  static const int MAINCOMPONENT_NODE_HEIGHT = 65;

  static const int BUFFERNODE_ICON_WIDTH     = 34;
  static const int BUFFERNODE_ICON_HEIGHT    = 34;
  static const int BUFFERNODE_NODE_WIDTH     = 65;
  static const int BUFFERNODE_NODE_HEIGHT    = 65;

  static const int DCM_ICON_WIDTH            = 34;
  static const int DCM_ICON_HEIGHT           = 34;
  static const int DCM_NODE_WIDTH            = 65;
  static const int DCM_NODE_HEIGHT           = 65;

};

} // end of namespace errorhandler
} // end of namespace novadaq

Q_DECLARE_METATYPE(novadaq::errorhandler::msgs_t)
Q_DECLARE_METATYPE(novadaq::errorhandler::msgs_sp_t)

#endif
