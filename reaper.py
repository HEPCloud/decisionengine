import decisionengine.framework.configmanager.ConfigManager as Conf_Manager
import decisionengine.framework.dataspace.dataspace as dataspace

if __name__ == "__main__":
    conf_manager = Conf_Manager.ConfigManager()
    conf_manager.load()
    reaper = dataspace.Reaper(config_manager.get_global_config())
