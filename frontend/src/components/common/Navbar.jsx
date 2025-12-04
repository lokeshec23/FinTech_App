/**
 * Navbar Component - Top Navigation with User Info
 */
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
    const { user, logout } = useAuth();

    const getInitials = (name) => {
        if (!name) return 'U';
        return name
            .split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/dashboard" className="navbar-brand">
                    <span className="brand-icon">₹</span>
                    <span className="brand-name">FinTech</span>
                </Link>

                <div className="navbar-right">
                    <div className="user-info">
                        <span className="user-name">{user?.name}</span>
                        <div className="user-avatar">
                            {getInitials(user?.name)}
                        </div>
                    </div>
                    <button onClick={logout} className="btn-logout">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        Sign Out
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
