import importlib
import pkgutil
import logging
import bot.modules as modules
from bot import get_application

logger = logging.getLogger(__name__)


def load_modules(application):
    for _, name, _ in pkgutil.iter_modules(modules.__path__, modules.__name__ + "."):
        try:
            module = importlib.import_module(name)
            if hasattr(module, "__init_module__"):
                module.__init_module__(application)
                logger.info(f"Loaded: {name}")
        except Exception as e:
            logger.exception(f"Error loading {name}: {e}")


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
