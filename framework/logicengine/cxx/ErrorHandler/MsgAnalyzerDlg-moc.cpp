/****************************************************************************
** Meta object code from reading C++ file 'MsgAnalyzerDlg.h'
**
** Created: Thu May 29 14:57:25 2014
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.4)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../include/MsgAnalyzerDlg.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'MsgAnalyzerDlg.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.4. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_novadaq__errorhandler__MsgAnalyzerDlg[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
      26,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
      39,   38,   38,   38, 0x08,
      54,   48,   38,   38, 0x08,
      92,   87,   38,   38, 0x08,
     157,  143,   38,   38, 0x08,
     190,  185,   38,   38, 0x08,
     216,   38,   38,   38, 0x08,
     224,   38,   38,   38, 0x08,
     236,  231,   38,   38, 0x08,
     272,  268,   38,   38, 0x08,
     303,  268,   38,   38, 0x08,
     333,  268,   38,   38, 0x08,
     363,   38,   38,   38, 0x08,
     384,   38,   38,   38, 0x08,
     407,   38,   38,   38, 0x08,
     428,   38,   38,   38, 0x08,
     439,   38,   38,   38, 0x08,
     450,   38,   38,   38, 0x08,
     467,   38,   38,   38, 0x08,
     481,   38,   38,   38, 0x08,
     496,   38,   38,   38, 0x08,
     523,  519,   38,   38, 0x08,
     539,   38,   38,   38, 0x08,
     567,  559,   38,   38, 0x08,
     584,  559,   38,   38, 0x08,
     611,  601,   38,   38, 0x08,
     647,  637,   38,   38, 0x08,

       0        // eod
};

static const char qt_meta_stringdata_novadaq__errorhandler__MsgAnalyzerDlg[] = {
    "novadaq::errorhandler::MsgAnalyzerDlg\0"
    "\0onLoad()\0mfmsg\0onNewMsg(mf::MessageFacilityMsg)\0"
    ",msg\0onNewSysMsg(mf::QtDDSReceiver::SysMsgCode,QString)\0"
    "rule_name,msg\0onNewAlarm(QString,QString)\0"
    "name\0onConditionMatch(QString)\0reset()\0"
    "exit()\0item\0onNodeClicked(QListWidgetItem*)\0"
    "pos\0show_main_context_menu(QPoint)\0"
    "show_dcm_context_menu(QPoint)\0"
    "show_evb_context_menu(QPoint)\0"
    "context_menu_reset()\0context_menu_warning()\0"
    "context_menu_error()\0open_log()\0"
    "read_log()\0read_completed()\0rule_enable()\0"
    "rule_disable()\0rule_reset_selection()\0"
    "idx\0reset_rule(int)\0reset_rule(QString)\0"
    "checked\0onRuleDesc(bool)\0onCondDesc(bool)\0"
    "partition\0onEstablishPartition(int)\0"
    "dcm,bnevb\0"
    "onSetParticipants(QVector<QString>,QVector<QString>)\0"
};

const QMetaObject novadaq::errorhandler::MsgAnalyzerDlg::staticMetaObject = {
    { &QDialog::staticMetaObject, qt_meta_stringdata_novadaq__errorhandler__MsgAnalyzerDlg,
      qt_meta_data_novadaq__errorhandler__MsgAnalyzerDlg, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &novadaq::errorhandler::MsgAnalyzerDlg::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *novadaq::errorhandler::MsgAnalyzerDlg::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *novadaq::errorhandler::MsgAnalyzerDlg::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_novadaq__errorhandler__MsgAnalyzerDlg))
        return static_cast<void*>(const_cast< MsgAnalyzerDlg*>(this));
    return QDialog::qt_metacast(_clname);
}

int novadaq::errorhandler::MsgAnalyzerDlg::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: onLoad(); break;
        case 1: onNewMsg((*reinterpret_cast< const mf::MessageFacilityMsg(*)>(_a[1]))); break;
        case 2: onNewSysMsg((*reinterpret_cast< mf::QtDDSReceiver::SysMsgCode(*)>(_a[1])),(*reinterpret_cast< const QString(*)>(_a[2]))); break;
        case 3: onNewAlarm((*reinterpret_cast< const QString(*)>(_a[1])),(*reinterpret_cast< const QString(*)>(_a[2]))); break;
        case 4: onConditionMatch((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 5: reset(); break;
        case 6: exit(); break;
        case 7: onNodeClicked((*reinterpret_cast< QListWidgetItem*(*)>(_a[1]))); break;
        case 8: show_main_context_menu((*reinterpret_cast< const QPoint(*)>(_a[1]))); break;
        case 9: show_dcm_context_menu((*reinterpret_cast< const QPoint(*)>(_a[1]))); break;
        case 10: show_evb_context_menu((*reinterpret_cast< const QPoint(*)>(_a[1]))); break;
        case 11: context_menu_reset(); break;
        case 12: context_menu_warning(); break;
        case 13: context_menu_error(); break;
        case 14: open_log(); break;
        case 15: read_log(); break;
        case 16: read_completed(); break;
        case 17: rule_enable(); break;
        case 18: rule_disable(); break;
        case 19: rule_reset_selection(); break;
        case 20: reset_rule((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 21: reset_rule((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 22: onRuleDesc((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 23: onCondDesc((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 24: onEstablishPartition((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 25: onSetParticipants((*reinterpret_cast< QVector<QString>(*)>(_a[1])),(*reinterpret_cast< QVector<QString>(*)>(_a[2]))); break;
        default: ;
        }
        _id -= 26;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
