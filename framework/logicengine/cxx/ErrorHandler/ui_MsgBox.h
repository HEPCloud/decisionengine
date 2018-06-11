/********************************************************************************
** Form generated from reading UI file 'MsgBox.ui'
**
** Created: Thu May 29 14:57:25 2014
**      by: Qt User Interface Compiler version 4.7.4
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MSGBOX_H
#define UI_MSGBOX_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QDialog>
#include <QtGui/QDialogButtonBox>
#include <QtGui/QFrame>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QPushButton>
#include <QtGui/QTextEdit>

QT_BEGIN_NAMESPACE

class Ui_MsgBox
{
public:
    QDialogButtonBox *buttonBox;
    QTextEdit *txtMessages;
    QPushButton *btnRefresh;
    QFrame *bannerFrame;
    QLabel *labelNodeName;
    QLabel *label_Partition_2;

    void setupUi(QDialog *MsgBox)
    {
        if (MsgBox->objectName().isEmpty())
            MsgBox->setObjectName(QString::fromUtf8("MsgBox"));
        MsgBox->resize(408, 443);
        MsgBox->setStyleSheet(QString::fromUtf8("#bannerFrame {\n"
"border: 0px;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#btnSettings {\n"
"color: #333;\n"
"border: 0px solid #555;\n"
"border-radius: 5px;\n"
"padding: 0px;\n"
"}\n"
"\n"
"#btnSettings:hover {\n"
"color: #444;\n"
"}\n"
"\n"
"#btnSwitchChannel {\n"
"color: #333;\n"
"border: 1px solid #555;\n"
"border-radius: 5px;\n"
"padding: 0px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
"}\n"
"#topFrame QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
"}\n"
"#topFrame QPushButton:pressed {\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
"}\n"
"\n"
"#sevFrame {\n"
"border: 0px solid #222;\n"
"background: ;\n"
"padding: 0px;\n"
"}"
                        "\n"
"\n"
"#mainFrame {\n"
"border: 0px;\n"
"background:\n"
"}\n"
"\n"
"#mainFrame QPushButton {\n"
"color: #333;\n"
"border: 1px solid #555;\n"
"border-radius: 3px;\n"
"padding: 0px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
"min-width: 80px;\n"
"}\n"
"\n"
"#mainFrame QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
"}\n"
"#mainFrame QPushButton:pressed {\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
"}\n"
"\n"
"#mainFrame QListWidget {\n"
"border: 1px solid #aaa;\n"
"background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:0.07, stop:0 rgba(220, 220, 200, 255), stop:1 rgba(255, 255, 230, 255))\n"
"}\n"
"\n"
"#mainFrame QTextEdit {\n"
"border: 1px solid #aaa;\n"
"background-color: #fff\n"
"}\n"
"\n"
"#btnError {\n"
"color: rgb(255, 0, 0);\n"
"}\n"
"#btnWarning {\n"
"color: "
                        "rgb(255, 170, 0);\n"
"}\n"
"#btnInfo {\n"
"color: rgb(0, 170, 0);\n"
"}\n"
"#btnDebug {\n"
"color: rgb(70, 70, 70);\n"
"}\n"
"\n"
"\n"
"/*\n"
"#sevFrame QPushButton {\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 5px;\n"
"padding: 2px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
"min-width: 80px;\n"
"}\n"
"#sevFrame QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
"}\n"
"#sevFrame QPushButton:pressed {\n"
"background: qradialgradient(cx: 0.4, cy: -0.1,\n"
"fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
"}*/"));
        buttonBox = new QDialogButtonBox(MsgBox);
        buttonBox->setObjectName(QString::fromUtf8("buttonBox"));
        buttonBox->setGeometry(QRect(310, 90, 91, 91));
        buttonBox->setOrientation(Qt::Vertical);
        buttonBox->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);
        txtMessages = new QTextEdit(MsgBox);
        txtMessages->setObjectName(QString::fromUtf8("txtMessages"));
        txtMessages->setGeometry(QRect(5, 45, 296, 391));
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(txtMessages->sizePolicy().hasHeightForWidth());
        txtMessages->setSizePolicy(sizePolicy);
        btnRefresh = new QPushButton(MsgBox);
        btnRefresh->setObjectName(QString::fromUtf8("btnRefresh"));
        btnRefresh->setGeometry(QRect(310, 45, 91, 27));
        bannerFrame = new QFrame(MsgBox);
        bannerFrame->setObjectName(QString::fromUtf8("bannerFrame"));
        bannerFrame->setGeometry(QRect(0, 0, 411, 36));
        bannerFrame->setFrameShape(QFrame::StyledPanel);
        bannerFrame->setFrameShadow(QFrame::Raised);
        labelNodeName = new QLabel(bannerFrame);
        labelNodeName->setObjectName(QString::fromUtf8("labelNodeName"));
        labelNodeName->setGeometry(QRect(170, 10, 181, 16));
        QPalette palette;
        QBrush brush(QColor(255, 255, 127, 255));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::WindowText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::WindowText, brush);
        QBrush brush1(QColor(118, 116, 113, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Disabled, QPalette::WindowText, brush1);
        labelNodeName->setPalette(palette);
        QFont font;
        font.setFamily(QString::fromUtf8("Sans Serif"));
        font.setBold(true);
        font.setWeight(75);
        labelNodeName->setFont(font);
        labelNodeName->setWordWrap(true);
        label_Partition_2 = new QLabel(bannerFrame);
        label_Partition_2->setObjectName(QString::fromUtf8("label_Partition_2"));
        label_Partition_2->setGeometry(QRect(10, 10, 161, 16));
        QPalette palette1;
        QBrush brush2(QColor(255, 255, 255, 255));
        brush2.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::WindowText, brush2);
        palette1.setBrush(QPalette::Inactive, QPalette::WindowText, brush2);
        QBrush brush3(QColor(133, 131, 127, 255));
        brush3.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Disabled, QPalette::WindowText, brush3);
        label_Partition_2->setPalette(palette1);
        QFont font1;
        font1.setFamily(QString::fromUtf8("Sans Serif"));
        font1.setPointSize(9);
        font1.setBold(false);
        font1.setWeight(50);
        label_Partition_2->setFont(font1);

        retranslateUi(MsgBox);
        QObject::connect(buttonBox, SIGNAL(accepted()), MsgBox, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), MsgBox, SLOT(reject()));

        QMetaObject::connectSlotsByName(MsgBox);
    } // setupUi

    void retranslateUi(QDialog *MsgBox)
    {
        MsgBox->setWindowTitle(QApplication::translate("MsgBox", "Node Details", 0, QApplication::UnicodeUTF8));
        btnRefresh->setText(QApplication::translate("MsgBox", "Refresh", 0, QApplication::UnicodeUTF8));
        labelNodeName->setText(QApplication::translate("MsgBox", "Node Name", 0, QApplication::UnicodeUTF8));
        label_Partition_2->setText(QApplication::translate("MsgBox", "Detailed Information for:", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MsgBox: public Ui_MsgBox {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MSGBOX_H
