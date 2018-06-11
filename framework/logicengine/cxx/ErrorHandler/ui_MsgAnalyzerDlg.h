/********************************************************************************
** Form generated from reading UI file 'MsgAnalyzerDlg.ui'
**
** Created: Thu May 29 14:57:25 2014
**      by: Qt User Interface Compiler version 4.7.4
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MSGANALYZERDLG_H
#define UI_MSGANALYZERDLG_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QDialog>
#include <QtGui/QFrame>
#include <QtGui/QGroupBox>
#include <QtGui/QHeaderView>
#include <QtGui/QLCDNumber>
#include <QtGui/QLabel>
#include <QtGui/QListWidget>
#include <QtGui/QProgressBar>
#include <QtGui/QPushButton>
#include <QtGui/QRadioButton>
#include <QtGui/QTabWidget>
#include <QtGui/QTableWidget>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MsgAnalyzerDlg
{
public:
    QFrame *bannerFrame;
    QLabel *label_Partition_3;
    QLabel *label_Partition_2;
    QLCDNumber *lcdMsgs;
    QPushButton *btnReset;
    QPushButton *btnExit;
    QFrame *mainFrame;
    QTabWidget *tabWidget;
    QWidget *tab_nodehealth;
    QListWidget *lwMain;
    QLabel *label;
    QListWidget *lwDCM;
    QLabel *label_2;
    QListWidget *lwBN;
    QLabel *label_3;
    QLabel *label_12;
    QWidget *tab_ruleengine;
    QLabel *label_8;
    QLabel *label_9;
    QTableWidget *twRules;
    QTableWidget *twConds;
    QFrame *frame;
    QRadioButton *rbRuleDesc;
    QRadioButton *rbRuleExpr;
    QLabel *label_10;
    QFrame *frame_2;
    QRadioButton *rbCondDesc;
    QRadioButton *rbCondRegx;
    QLabel *label_11;
    QPushButton *btnRuleAct;
    QPushButton *btnCondAct;
    QListWidget *lwAlerts;
    QGroupBox *groupBox;
    QProgressBar *pbLog;
    QPushButton *btnReadLog;
    QPushButton *btnOpenLog;
    QLabel *labelLogFile;

    void setupUi(QDialog *MsgAnalyzerDlg)
    {
        if (MsgAnalyzerDlg->objectName().isEmpty())
            MsgAnalyzerDlg->setObjectName(QString::fromUtf8("MsgAnalyzerDlg"));
        MsgAnalyzerDlg->resize(998, 700);
        MsgAnalyzerDlg->setStyleSheet(QString::fromUtf8("#bannerFrame {\n"
"border: 0px;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#bannerFrame QPushButton {\n"
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
"background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.3"
                        "5, stop: 0 #fff, stop: 1 #ddd);\n"
"}\n"
"#topFrame QPushButton:pressed {\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
"}\n"
"\n"
"#sevFrame {\n"
"border: 0px solid #222;\n"
"background: ;\n"
"padding: 0px;\n"
"}\n"
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
"min-width: 40px;\n"
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
"background-color: qlineargradient(spread:pad, x1:0.5, "
                        "y1:0, x2:0.5, y2:0.07, stop:0 rgba(220, 220, 200, 255), stop:1 rgba(255, 255, 230, 255))\n"
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
"color: rgb(255, 170, 0);\n"
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
        bannerFrame = new QFrame(MsgAnalyzerDlg);
        bannerFrame->setObjectName(QString::fromUtf8("bannerFrame"));
        bannerFrame->setGeometry(QRect(0, 0, 1011, 51));
        bannerFrame->setFrameShape(QFrame::StyledPanel);
        bannerFrame->setFrameShadow(QFrame::Raised);
        label_Partition_3 = new QLabel(bannerFrame);
        label_Partition_3->setObjectName(QString::fromUtf8("label_Partition_3"));
        label_Partition_3->setGeometry(QRect(10, 10, 211, 27));
        QPalette palette;
        QBrush brush(QColor(255, 170, 0, 255));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::WindowText, brush);
        palette.setBrush(QPalette::Inactive, QPalette::WindowText, brush);
        QBrush brush1(QColor(133, 131, 127, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Disabled, QPalette::WindowText, brush1);
        label_Partition_3->setPalette(palette);
        QFont font;
        font.setFamily(QString::fromUtf8("Sans Serif"));
        font.setPointSize(11);
        font.setBold(true);
        font.setWeight(75);
        label_Partition_3->setFont(font);
        label_Partition_3->setAutoFillBackground(false);
        label_Partition_2 = new QLabel(bannerFrame);
        label_Partition_2->setObjectName(QString::fromUtf8("label_Partition_2"));
        label_Partition_2->setGeometry(QRect(500, 10, 161, 27));
        QPalette palette1;
        QBrush brush2(QColor(255, 255, 255, 255));
        brush2.setStyle(Qt::SolidPattern);
        palette1.setBrush(QPalette::Active, QPalette::WindowText, brush2);
        palette1.setBrush(QPalette::Inactive, QPalette::WindowText, brush2);
        palette1.setBrush(QPalette::Disabled, QPalette::WindowText, brush1);
        label_Partition_2->setPalette(palette1);
        QFont font1;
        font1.setFamily(QString::fromUtf8("Sans Serif"));
        font1.setPointSize(10);
        font1.setBold(false);
        font1.setWeight(50);
        label_Partition_2->setFont(font1);
        lcdMsgs = new QLCDNumber(bannerFrame);
        lcdMsgs->setObjectName(QString::fromUtf8("lcdMsgs"));
        lcdMsgs->setGeometry(QRect(660, 10, 100, 27));
        QPalette palette2;
        QBrush brush3(QColor(0, 255, 0, 255));
        brush3.setStyle(Qt::SolidPattern);
        palette2.setBrush(QPalette::Active, QPalette::WindowText, brush3);
        palette2.setBrush(QPalette::Inactive, QPalette::WindowText, brush3);
        palette2.setBrush(QPalette::Disabled, QPalette::WindowText, brush1);
        lcdMsgs->setPalette(palette2);
        lcdMsgs->setFrameShape(QFrame::Box);
        lcdMsgs->setFrameShadow(QFrame::Raised);
        lcdMsgs->setSmallDecimalPoint(false);
        lcdMsgs->setNumDigits(8);
        lcdMsgs->setSegmentStyle(QLCDNumber::Flat);
        btnReset = new QPushButton(bannerFrame);
        btnReset->setObjectName(QString::fromUtf8("btnReset"));
        btnReset->setGeometry(QRect(780, 10, 98, 27));
        btnExit = new QPushButton(bannerFrame);
        btnExit->setObjectName(QString::fromUtf8("btnExit"));
        btnExit->setGeometry(QRect(890, 10, 98, 27));
        mainFrame = new QFrame(MsgAnalyzerDlg);
        mainFrame->setObjectName(QString::fromUtf8("mainFrame"));
        mainFrame->setGeometry(QRect(0, 50, 1001, 651));
        mainFrame->setFrameShape(QFrame::StyledPanel);
        mainFrame->setFrameShadow(QFrame::Raised);
        tabWidget = new QTabWidget(mainFrame);
        tabWidget->setObjectName(QString::fromUtf8("tabWidget"));
        tabWidget->setGeometry(QRect(370, 10, 611, 541));
        tab_nodehealth = new QWidget();
        tab_nodehealth->setObjectName(QString::fromUtf8("tab_nodehealth"));
        lwMain = new QListWidget(tab_nodehealth);
        lwMain->setObjectName(QString::fromUtf8("lwMain"));
        lwMain->setGeometry(QRect(10, 30, 591, 131));
        QFont font2;
        font2.setPointSize(8);
        lwMain->setFont(font2);
        lwMain->setContextMenuPolicy(Qt::CustomContextMenu);
        lwMain->setFrameShape(QFrame::StyledPanel);
        lwMain->setFrameShadow(QFrame::Sunken);
        lwMain->setProperty("isWrapping", QVariant(true));
        lwMain->setGridSize(QSize(80, 60));
        lwMain->setViewMode(QListView::IconMode);
        lwMain->setWordWrap(true);
        label = new QLabel(tab_nodehealth);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(10, 10, 161, 17));
        QFont font3;
        font3.setFamily(QString::fromUtf8("Sans Serif"));
        font3.setPointSize(10);
        font3.setBold(true);
        font3.setWeight(75);
        label->setFont(font3);
        lwDCM = new QListWidget(tab_nodehealth);
        lwDCM->setObjectName(QString::fromUtf8("lwDCM"));
        lwDCM->setGeometry(QRect(10, 200, 291, 301));
        lwDCM->setFont(font2);
        lwDCM->setContextMenuPolicy(Qt::CustomContextMenu);
        lwDCM->setViewMode(QListView::IconMode);
        lwDCM->setUniformItemSizes(false);
        lwDCM->setBatchSize(100);
        lwDCM->setWordWrap(true);
        label_2 = new QLabel(tab_nodehealth);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(10, 180, 211, 17));
        QFont font4;
        font4.setFamily(QString::fromUtf8("Sans Serif"));
        font4.setBold(true);
        font4.setWeight(75);
        label_2->setFont(font4);
        lwBN = new QListWidget(tab_nodehealth);
        lwBN->setObjectName(QString::fromUtf8("lwBN"));
        lwBN->setGeometry(QRect(310, 200, 291, 301));
        lwBN->setFont(font2);
        lwBN->setContextMenuPolicy(Qt::CustomContextMenu);
        lwBN->setViewMode(QListView::IconMode);
        label_3 = new QLabel(tab_nodehealth);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(310, 180, 181, 17));
        label_3->setFont(font4);
        label_12 = new QLabel(tab_nodehealth);
        label_12->setObjectName(QString::fromUtf8("label_12"));
        label_12->setGeometry(QRect(300, 10, 301, 20));
        tabWidget->addTab(tab_nodehealth, QString());
        tab_ruleengine = new QWidget();
        tab_ruleengine->setObjectName(QString::fromUtf8("tab_ruleengine"));
        label_8 = new QLabel(tab_ruleengine);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        label_8->setGeometry(QRect(10, 250, 141, 17));
        label_8->setFont(font4);
        label_9 = new QLabel(tab_ruleengine);
        label_9->setObjectName(QString::fromUtf8("label_9"));
        label_9->setGeometry(QRect(10, 10, 141, 17));
        label_9->setFont(font4);
        twRules = new QTableWidget(tab_ruleengine);
        if (twRules->columnCount() < 4)
            twRules->setColumnCount(4);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        twRules->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        twRules->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        twRules->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        twRules->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        twRules->setObjectName(QString::fromUtf8("twRules"));
        twRules->setGeometry(QRect(10, 30, 591, 201));
        twRules->setEditTriggers(QAbstractItemView::NoEditTriggers);
        twRules->setSelectionBehavior(QAbstractItemView::SelectRows);
        twRules->setColumnCount(4);
        twConds = new QTableWidget(tab_ruleengine);
        if (twConds->columnCount() < 4)
            twConds->setColumnCount(4);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        twConds->setHorizontalHeaderItem(0, __qtablewidgetitem4);
        QTableWidgetItem *__qtablewidgetitem5 = new QTableWidgetItem();
        twConds->setHorizontalHeaderItem(1, __qtablewidgetitem5);
        QTableWidgetItem *__qtablewidgetitem6 = new QTableWidgetItem();
        twConds->setHorizontalHeaderItem(2, __qtablewidgetitem6);
        QTableWidgetItem *__qtablewidgetitem7 = new QTableWidgetItem();
        __qtablewidgetitem7->setTextAlignment(Qt::AlignRight|Qt::AlignVCenter);
        twConds->setHorizontalHeaderItem(3, __qtablewidgetitem7);
        twConds->setObjectName(QString::fromUtf8("twConds"));
        twConds->setGeometry(QRect(10, 270, 591, 231));
        twConds->setEditTriggers(QAbstractItemView::NoEditTriggers);
        twConds->setSelectionBehavior(QAbstractItemView::SelectRows);
        twConds->setColumnCount(4);
        frame = new QFrame(tab_ruleengine);
        frame->setObjectName(QString::fromUtf8("frame"));
        frame->setGeometry(QRect(230, 10, 291, 21));
        frame->setFrameShape(QFrame::NoFrame);
        frame->setFrameShadow(QFrame::Plain);
        frame->setLineWidth(0);
        rbRuleDesc = new QRadioButton(frame);
        rbRuleDesc->setObjectName(QString::fromUtf8("rbRuleDesc"));
        rbRuleDesc->setGeometry(QRect(60, 0, 111, 22));
        rbRuleDesc->setChecked(true);
        rbRuleExpr = new QRadioButton(frame);
        rbRuleExpr->setObjectName(QString::fromUtf8("rbRuleExpr"));
        rbRuleExpr->setGeometry(QRect(170, 0, 101, 22));
        rbRuleExpr->setChecked(false);
        label_10 = new QLabel(frame);
        label_10->setObjectName(QString::fromUtf8("label_10"));
        label_10->setGeometry(QRect(0, 0, 51, 22));
        frame_2 = new QFrame(tab_ruleengine);
        frame_2->setObjectName(QString::fromUtf8("frame_2"));
        frame_2->setGeometry(QRect(230, 250, 291, 21));
        frame_2->setFrameShape(QFrame::NoFrame);
        frame_2->setFrameShadow(QFrame::Plain);
        frame_2->setLineWidth(0);
        rbCondDesc = new QRadioButton(frame_2);
        rbCondDesc->setObjectName(QString::fromUtf8("rbCondDesc"));
        rbCondDesc->setGeometry(QRect(60, 0, 111, 22));
        rbCondDesc->setChecked(true);
        rbCondRegx = new QRadioButton(frame_2);
        rbCondRegx->setObjectName(QString::fromUtf8("rbCondRegx"));
        rbCondRegx->setGeometry(QRect(170, 0, 101, 22));
        label_11 = new QLabel(frame_2);
        label_11->setObjectName(QString::fromUtf8("label_11"));
        label_11->setGeometry(QRect(0, 0, 51, 22));
        btnRuleAct = new QPushButton(tab_ruleengine);
        btnRuleAct->setObjectName(QString::fromUtf8("btnRuleAct"));
        btnRuleAct->setGeometry(QRect(520, 10, 82, 17));
        btnCondAct = new QPushButton(tab_ruleengine);
        btnCondAct->setObjectName(QString::fromUtf8("btnCondAct"));
        btnCondAct->setGeometry(QRect(520, 250, 82, 17));
        tabWidget->addTab(tab_ruleengine, QString());
        lwAlerts = new QListWidget(mainFrame);
        lwAlerts->setObjectName(QString::fromUtf8("lwAlerts"));
        lwAlerts->setGeometry(QRect(10, 10, 351, 621));
        QFont font5;
        lwAlerts->setFont(font5);
        lwAlerts->setStyleSheet(QString::fromUtf8("border: 1px solid #aaa;\n"
"background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:0.015, stop:0 rgba(220, 220, 200, 255), stop:1 rgba(255, 255, 240, 255));\n"
"font-size: 12px;\n"
"/*color: red;*/"));
        lwAlerts->setFrameShape(QFrame::StyledPanel);
        lwAlerts->setFrameShadow(QFrame::Sunken);
        lwAlerts->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        lwAlerts->setProperty("isWrapping", QVariant(false));
        lwAlerts->setViewMode(QListView::ListMode);
        lwAlerts->setWordWrap(true);
        groupBox = new QGroupBox(mainFrame);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        groupBox->setGeometry(QRect(370, 560, 611, 71));
        pbLog = new QProgressBar(groupBox);
        pbLog->setObjectName(QString::fromUtf8("pbLog"));
        pbLog->setGeometry(QRect(20, 40, 401, 23));
        pbLog->setValue(24);
        btnReadLog = new QPushButton(groupBox);
        btnReadLog->setObjectName(QString::fromUtf8("btnReadLog"));
        btnReadLog->setGeometry(QRect(520, 40, 82, 21));
        btnOpenLog = new QPushButton(groupBox);
        btnOpenLog->setObjectName(QString::fromUtf8("btnOpenLog"));
        btnOpenLog->setGeometry(QRect(430, 40, 82, 21));
        labelLogFile = new QLabel(groupBox);
        labelLogFile->setObjectName(QString::fromUtf8("labelLogFile"));
        labelLogFile->setGeometry(QRect(20, 20, 581, 20));
        QFont font6;
        font6.setFamily(QString::fromUtf8("Bitstream Vera Sans Mono"));
        labelLogFile->setFont(font6);

        retranslateUi(MsgAnalyzerDlg);

        tabWidget->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(MsgAnalyzerDlg);
    } // setupUi

    void retranslateUi(QDialog *MsgAnalyzerDlg)
    {
        MsgAnalyzerDlg->setWindowTitle(QApplication::translate("MsgAnalyzerDlg", "NOvA Message Analyzer", 0, QApplication::UnicodeUTF8));
        label_Partition_3->setText(QApplication::translate("MsgAnalyzerDlg", "NOvA Message Analyzer", 0, QApplication::UnicodeUTF8));
        label_Partition_2->setText(QApplication::translate("MsgAnalyzerDlg", "Total parsed messages", 0, QApplication::UnicodeUTF8));
        btnReset->setText(QApplication::translate("MsgAnalyzerDlg", "Reset All", 0, QApplication::UnicodeUTF8));
        btnExit->setText(QApplication::translate("MsgAnalyzerDlg", "Exit", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("MsgAnalyzerDlg", "Main Components", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("MsgAnalyzerDlg", "Data Concentrate Modules", 0, QApplication::UnicodeUTF8));
        label_3->setText(QApplication::translate("MsgAnalyzerDlg", "Buffer Node EVBs", 0, QApplication::UnicodeUTF8));
        label_12->setText(QApplication::translate("MsgAnalyzerDlg", "Double click on nodes for detailed messages", 0, QApplication::UnicodeUTF8));
        tabWidget->setTabText(tabWidget->indexOf(tab_nodehealth), QApplication::translate("MsgAnalyzerDlg", "Node Status", 0, QApplication::UnicodeUTF8));
        label_8->setText(QApplication::translate("MsgAnalyzerDlg", "Base conditions", 0, QApplication::UnicodeUTF8));
        label_9->setText(QApplication::translate("MsgAnalyzerDlg", "Rules", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem = twRules->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QApplication::translate("MsgAnalyzerDlg", "Name", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem1 = twRules->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QApplication::translate("MsgAnalyzerDlg", "Details", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem2 = twRules->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QApplication::translate("MsgAnalyzerDlg", "Status", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem3 = twRules->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QApplication::translate("MsgAnalyzerDlg", "Rst", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem4 = twConds->horizontalHeaderItem(0);
        ___qtablewidgetitem4->setText(QApplication::translate("MsgAnalyzerDlg", "Name", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem5 = twConds->horizontalHeaderItem(1);
        ___qtablewidgetitem5->setText(QApplication::translate("MsgAnalyzerDlg", "From", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem6 = twConds->horizontalHeaderItem(2);
        ___qtablewidgetitem6->setText(QApplication::translate("MsgAnalyzerDlg", "Details", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem7 = twConds->horizontalHeaderItem(3);
        ___qtablewidgetitem7->setText(QApplication::translate("MsgAnalyzerDlg", "Cnt", 0, QApplication::UnicodeUTF8));
        rbRuleDesc->setText(QApplication::translate("MsgAnalyzerDlg", "Description", 0, QApplication::UnicodeUTF8));
        rbRuleExpr->setText(QApplication::translate("MsgAnalyzerDlg", "Expression", 0, QApplication::UnicodeUTF8));
        label_10->setText(QApplication::translate("MsgAnalyzerDlg", "Details", 0, QApplication::UnicodeUTF8));
        rbCondDesc->setText(QApplication::translate("MsgAnalyzerDlg", "Description", 0, QApplication::UnicodeUTF8));
        rbCondRegx->setText(QApplication::translate("MsgAnalyzerDlg", "RegExpr", 0, QApplication::UnicodeUTF8));
        label_11->setText(QApplication::translate("MsgAnalyzerDlg", "Details", 0, QApplication::UnicodeUTF8));
        btnRuleAct->setText(QApplication::translate("MsgAnalyzerDlg", "Actions", 0, QApplication::UnicodeUTF8));
        btnCondAct->setText(QApplication::translate("MsgAnalyzerDlg", "Actions", 0, QApplication::UnicodeUTF8));
        tabWidget->setTabText(tabWidget->indexOf(tab_ruleengine), QApplication::translate("MsgAnalyzerDlg", "Rule Engine Indicator", 0, QApplication::UnicodeUTF8));
        groupBox->setTitle(QApplication::translate("MsgAnalyzerDlg", "Message Log Analyzer", 0, QApplication::UnicodeUTF8));
        btnReadLog->setText(QApplication::translate("MsgAnalyzerDlg", "Start", 0, QApplication::UnicodeUTF8));
        btnOpenLog->setText(QApplication::translate("MsgAnalyzerDlg", "Open", 0, QApplication::UnicodeUTF8));
        labelLogFile->setText(QApplication::translate("MsgAnalyzerDlg", "Click open to select an archived log file", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MsgAnalyzerDlg: public Ui_MsgAnalyzerDlg {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MSGANALYZERDLG_H
