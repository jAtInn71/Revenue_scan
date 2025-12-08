import { useState, useEffect } from 'react';
import { getCurrentUser, updateProfile, changePassword } from '../services/api';

const Settings = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  
  const [profileData, setProfileData] = useState({
    full_name: '',
    company_name: '',
    role: '',
  });

  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData);
      setProfileData({
        full_name: userData.full_name || '',
        company_name: userData.company_name || '',
        role: userData.role || '',
      });
    } catch (error) {
      console.error('Failed to load user:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    try {
      await updateProfile(profileData);
      setMessage('Profile updated successfully!');
      loadUser();
    } catch (error) {
      setMessage('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setMessage('');

    if (passwordData.new_password !== passwordData.confirm_password) {
      setMessage('Passwords do not match');
      return;
    }

    if (passwordData.new_password.length < 6) {
      setMessage('Password must be at least 6 characters');
      return;
    }

    setSaving(true);

    try {
      await changePassword({
        current_password: passwordData.current_password,
        new_password: passwordData.new_password,
      });
      setMessage('Password changed successfully!');
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
    } catch (error) {
      setMessage('Failed to change password');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-12 h-12 border-4 border-brand-accent border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-black">Settings</h1>
        <p className="text-slate-600 mt-2">Manage your account settings</p>
      </div>

      {/* Message */}
      {message && (
        <div className={`p-4 rounded-lg font-medium ${message.includes('success') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
          {message}
        </div>
      )}

      {/* Profile Settings */}
      <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6">
        <h2 className="text-lg sm:text-xl font-bold text-black mb-6">Profile Information</h2>
        
        <form onSubmit={handleProfileUpdate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">Email</label>
            <input
              type="email"
              value={user?.email || ''}
              disabled
              className="w-full px-4 py-3 border border-slate-300 rounded-lg bg-slate-50 text-slate-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">Full Name</label>
            <input
              type="text"
              value={profileData.full_name}
              onChange={(e) => setProfileData({ ...profileData, full_name: e.target.value })}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">Company Name</label>
            <input
              type="text"
              value={profileData.company_name}
              onChange={(e) => setProfileData({ ...profileData, company_name: e.target.value })}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">Role</label>
            <select
              value={profileData.role}
              onChange={(e) => setProfileData({ ...profileData, role: e.target.value })}
              className="input-field"
            >
              <option value="">Select Role</option>
              <option value="CFO">CFO</option>
              <option value="Finance Manager">Finance Manager</option>
              <option value="Revenue Analyst">Revenue Analyst</option>
              <option value="Business Owner">Business Owner</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={saving}
            className="w-full px-6 py-3 bg-black text-brand-accent rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Saving...' : 'Update Profile'}
          </button>
        </form>
      </div>

      {/* Password Settings */}
      <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6">
        <h2 className="text-lg sm:text-xl font-bold text-black mb-6">Change Password</h2>
        
        <form onSubmit={handlePasswordChange} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">Current Password</label>
            <input
              type="password"
              value={passwordData.current_password}
              onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">New Password</label>
            <input
              type="password"
              value={passwordData.new_password}
              onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-900 mb-2">Confirm New Password</label>
            <input
              type="password"
              value={passwordData.confirm_password}
              onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
              className="input-field"
            />
          </div>

          <button
            type="submit"
            disabled={saving}
            className="w-full px-6 py-3 bg-black text-brand-accent rounded-lg font-semibold hover:bg-slate-900 shadow-md transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Changing...' : 'Change Password'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Settings;
