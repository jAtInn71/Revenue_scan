import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { getCurrentUser, getNotifications, logout } from '../services/api';
import { 
  MdDashboard, MdFileUpload, MdRocket, MdAnalytics, 
  MdSmartToy, MdNotifications, MdBarChart, MdSettings,
  MdMenu, MdClose, MdHistory
} from 'react-icons/md';
import { IoMdArrowDropdown } from 'react-icons/io';

// Modern Logo Component
const Logo = () => (
  <div className="flex items-center gap-2 md:gap-3 animate-fade-in">
    <div className="w-8 h-8 md:w-10 md:h-10 bg-black rounded-lg flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow duration-300 group">
      <svg viewBox="0 0 40 40" className="w-5 h-5 md:w-6 md:h-6">
        {/* Modern R design */}
        <defs>
          <linearGradient id="rGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#ffffff', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#f0f0f0', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        {/* Vertical bar */}
        <rect x="10" y="8" width="4" height="24" fill="url(#rGradient)" rx="2" />
        {/* Top curve */}
        <path d="M 14 8 Q 22 8 22 14 Q 22 18 14 18" fill="none" stroke="url(#rGradient)" strokeWidth="4" strokeLinecap="round" />
        {/* Bottom diagonal leg */}
        <line x1="14" y1="18" x2="26" y2="32" stroke="url(#rGradient)" strokeWidth="4" strokeLinecap="round" />
      </svg>
    </div>
    <div>
      <h1 className="text-lg md:text-xl font-bold text-black group-hover:text-gray-800 transition-colors duration-300">
        Revenue
      </h1>
      <p className="text-xs text-gray-500 hidden sm:block font-semibold tracking-wide">AI Analytics</p>
    </div>
  </div>
);

const Layout = ({ setIsAuthenticated }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    loadUser();
    loadNotifications();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
      // Silently fail - user will be null
    }
  };

  const loadNotifications = async () => {
    try {
      const data = await getNotifications();
      setNotifications(data && Array.isArray(data) ? data.slice(0, 5) : []);
    } catch (error) {
      console.error('Failed to load notifications:', error);
      // Silently fail - notifications will be empty
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      localStorage.removeItem('token');
      setIsAuthenticated(false);
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const navigation = [
    { name: 'Dashboard', path: '/dashboard', icon: MdDashboard },
    { name: 'Upload Data', path: '/upload', icon: MdFileUpload },
    { name: 'New Business', path: '/analyze/new-business', icon: MdRocket },
    { name: 'Existing Business', path: '/analyze/existing-business', icon: MdAnalytics },
    { name: 'AI Insights', path: '/ai-chat', icon: MdSmartToy },
    { name: 'Reports', path: '/reports', icon: MdBarChart },
    ...(user?.role === 'admin' ? [
      { name: 'Admin Panel', path: '/admin', icon: MdSettings },
      { name: 'History', path: '/history', icon: MdHistory }
    ] : []),
    { name: 'Settings', path: '/settings', icon: MdSettings },
  ];

  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white border-b border-gray-200 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow duration-300">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16 md:h-20">
            {/* Left: Logo & Sidebar Toggle */}
            <div className="flex items-center gap-3 md:gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-all duration-200 transform hover:scale-110 active:scale-95"
              >
                {sidebarOpen ? (
                  <MdClose className="w-6 h-6 text-black animate-scale-in" />
                ) : (
                  <MdMenu className="w-6 h-6 text-black animate-scale-in" />
                )}
              </button>
              
              <Logo />
            </div>

            {/* Right: Notifications & User Menu */}
            <div className="flex items-center gap-2 md:gap-4">
              {/* Notifications */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="relative p-2 text-gray-600 hover:text-black hover:bg-gray-50 rounded-lg transition-all duration-200 transform hover:scale-110 active:scale-95"
                >
                  <MdNotifications className="w-6 h-6" />
                  {unreadCount > 0 && (
                    <span className="absolute top-0 right-0 w-5 h-5 bg-black text-white text-xs rounded-full flex items-center justify-center font-bold animate-bounce-soft">
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                  )}
                </button>

                {showNotifications && (
                  <div className="absolute right-0 mt-2 w-96 max-w-[calc(100vw-32px)] bg-white rounded-xl shadow-2xl border border-gray-200 py-2 max-h-96 overflow-y-auto z-50 animate-slide-down">
                    <div className="px-4 py-3 border-b border-gray-100 sticky top-0 bg-white">
                      <h3 className="font-semibold text-black">Notifications</h3>
                    </div>
                    {notifications.length === 0 ? (
                      <p className="px-4 py-8 text-center text-gray-500">No notifications</p>
                    ) : (
                      notifications.map((notif, idx) => (
                        <div key={idx} className={`px-4 py-3 border-b border-gray-50 hover:bg-gray-50 cursor-pointer transition-all duration-200 ${!notif.is_read ? 'bg-gray-100' : ''}`}>
                          <p className="text-sm font-medium text-black">{notif.title}</p>
                          <p className="text-xs text-gray-600 mt-1">{notif.message}</p>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>

              {/* User menu */}
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 px-2 md:px-3 py-2 rounded-lg hover:bg-gray-50 transition-all duration-200 transform hover:scale-105 active:scale-95"
                >
                  <div className="w-8 h-8 md:w-9 md:h-9 bg-black text-white rounded-full flex items-center justify-center font-semibold text-sm group-hover:shadow-lg transition-all duration-300">
                    {user?.full_name?.charAt(0) || 'U'}
                  </div>
                  <span className="text-sm font-medium text-gray-700 hidden md:inline">{user?.full_name?.split(' ')[0] || 'User'}</span>
                  <IoMdArrowDropdown className={`w-4 h-4 text-gray-600 transition-transform duration-300 ${showUserMenu ? 'rotate-180' : ''}`} />
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-2xl border border-gray-200 py-2 z-50 animate-slide-down">
                    <Link
                      to="/settings"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-black hover:bg-gray-50 transition-all duration-200"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <MdSettings className="w-4 h-4" />
                      Settings
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="flex items-center gap-3 w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 transition-all duration-200"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`fixed md:relative z-40 w-64 h-[calc(100vh-64px)] md:h-[calc(100vh-80px)] bg-white border-r border-gray-200 overflow-y-auto transition-all duration-300 ${
          sidebarOpen ? 'translate-x-0 shadow-lg md:shadow-none' : '-translate-x-full md:translate-x-0'
        }`}>
          <nav className="p-4 space-y-2">
            {navigation.map((item) => {
              const IconComponent = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all duration-300 transform ${
                    isActive
                      ? 'bg-black text-white shadow-lg scale-105 animate-slide-right'
                      : 'text-gray-700 hover:bg-gray-100 hover:text-black'
                  }`}
                >
                  <IconComponent className="w-5 h-5 md:w-6 md:h-6" />
                  <span className="text-sm md:text-base">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/40 md:hidden z-30 animate-fade-in"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 w-full overflow-x-hidden animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
