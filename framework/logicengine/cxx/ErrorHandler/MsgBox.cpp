
#include <ErrorHandler/MsgBox.h>

using namespace novadaq::errorhandler;

MsgBox::MsgBox( QString const & title, NodeInfo const & info, QDialog * parent)
: node (info)
{
  setupUi(this);

  connect( btnRefresh, SIGNAL( clicked() ), this, SLOT( refreshMsgs() ) );

  // write node name
  labelNodeName->setText(title);

  // print messages
  txtMessages->setHtml(node.msgs_to_string());
  txtMessages->moveCursor(QTextCursor::End);
}

void MsgBox::refreshMsgs()
{
  txtMessages->clear();
  txtMessages->setHtml(node.msgs_to_string());
  txtMessages->moveCursor(QTextCursor::End);
}

