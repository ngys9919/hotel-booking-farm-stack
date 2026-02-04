import { useState, useEffect } from 'react';
import { api } from '../api';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingUser, setEditingUser] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const data = await api.getAllUsers();
      setUsers(data);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateUser = async (userId, updateData) => {
    try {
      await api.updateUser(userId, updateData);
      await fetchUsers();
      setEditingUser(null);
      alert('User updated successfully!');
    } catch (err) {
      alert(err.message || 'Failed to update user');
    }
  };

  const handleDeleteUser = async (userId, userEmail) => {
    if (!confirm(`Are you sure you want to delete user ${userEmail}?`)) {
      return;
    }
    
    try {
      await api.deleteUser(userId);
      await fetchUsers();
      alert('User deleted successfully!');
    } catch (err) {
      alert(err.message || 'Failed to delete user');
    }
  };

  const handleToggleActive = async (user) => {
    try {
      await api.updateUser(user.id, { is_active: !user.is_active });
      await fetchUsers();
    } catch (err) {
      alert(err.message || 'Failed to update user status');
    }
  };

  const handleToggleRole = async (user) => {
    const newRole = user.role === 'admin' ? 'user' : 'admin';
    if (!confirm(`Change ${user.email}'s role to ${newRole}?`)) {
      return;
    }
    
    try {
      await api.updateUser(user.id, { role: newRole });
      await fetchUsers();
    } catch (err) {
      alert(err.message || 'Failed to update user role');
    }
  };

  const filteredUsers = users.filter(user =>
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.full_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="admin-page">
        <div className="loading-spinner">Loading users...</div>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>User Management</h1>
        <p>Manage all registered users</p>
      </div>

      <div className="page-controls">
        <input
          type="text"
          placeholder="Search by email or name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <button onClick={fetchUsers} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="users-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Email</th>
              <th>Full Name</th>
              <th>Role</th>
              <th>Status</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((user) => (
              <tr key={user.id}>
                <td>{user.email}</td>
                <td>{user.full_name}</td>
                <td>
                  <span className={`role-badge ${user.role}`}>
                    {user.role}
                  </span>
                </td>
                <td>
                  <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td className="action-buttons">
                  <button
                    onClick={() => handleToggleActive(user)}
                    className="btn-small"
                    title={user.is_active ? 'Deactivate' : 'Activate'}
                  >
                    {user.is_active ? '🔒' : '🔓'}
                  </button>
                  <button
                    onClick={() => handleToggleRole(user)}
                    className="btn-small"
                    title={`Change to ${user.role === 'admin' ? 'user' : 'admin'}`}
                  >
                    {user.role === 'admin' ? '👤' : '👑'}
                  </button>
                  <button
                    onClick={() => handleDeleteUser(user.id, user.email)}
                    className="btn-small btn-danger"
                    title="Delete user"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredUsers.length === 0 && !loading && (
        <div className="empty-state">
          <p>No users found</p>
        </div>
      )}

      <div className="page-footer">
        <p>Total users: {filteredUsers.length}</p>
      </div>
    </div>
  );
};

export default UserManagement;
