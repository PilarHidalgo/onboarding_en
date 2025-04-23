
from ui.pages.inventory_page import InventoryPage
from ui.pages.add_fruit_page import AddFruitPage
from ui.pages.update_fruit_page import UpdateFruitPage
from ui.pages.delete_fruit_page import DeleteFruitPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.settings_page import SettingsPage
from ui.pages.about_page import AboutPage
from ui.pages.login_page import LoginPage

# Dictionary mapping page names to page classes
# This is used by the application controller to create page instances
PAGE_CLASSES = {
    "InventoryPage": InventoryPage,
    "AddFruitPage": AddFruitPage,
    "UpdateFruitPage": UpdateFruitPage,
    "DeleteFruitPage": DeleteFruitPage,
    "DashboardPage": DashboardPage,
    "SettingsPage": SettingsPage,
    "AboutPage": AboutPage,
    "LoginPage": LoginPage
}

__all__ = [
    'InventoryPage',
    'AddFruitPage',
    'UpdateFruitPage',
    'DeleteFruitPage',
    'DashboardPage',
    'SettingsPage',
    'AboutPage',
    'LoginPage',
    'PAGE_CLASSES'
]