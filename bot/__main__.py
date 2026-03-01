import importlib
import pkgutil
import logging
import bot.modules as modules
from bot import get_application

logger = logging.getLogger(__name__)


def load_modules(application):
    def _load(package):
        for _, name, ispkg in pkgutil.iter_modules(
            package.__path__, package.__name__ + "."
        ):
            try:
                mod = importlib.import_module(name)
                if ispkg:
                    _load(mod)
                elif hasattr(mod, "__init_module__"):
                    mod.__init_module__(application)
                    logger.info(f"Loaded: {name}")
            except Exception as e:
                logger.exception(f"Error loading {name}: {e}")

    _load(modules)


def main():
    try:
        application = get_application()
        load_modules(application)
        logger.info("Bot running...")
        application.run_polling()
    except KeyboardInterrupt:
        logger.info("Stopped.")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
