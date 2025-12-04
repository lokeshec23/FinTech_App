/**
 * Sidebar Navigation Component
 */
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
    const navItems = [
        { path: '/dashboard', icon: '📊', label: 'Dashboard' },
        { path: '/expenses', icon: '💰', label: 'Expenses' },
        { path: '/emis', icon: '📅', label: 'EMIs' },
        { path: '/bank-accounts', icon: '🏦', label: 'Bank Accounts' },
        { path: '/assets', icon: '📈', label: 'Assets' },
        { path: '/liabilities', icon: '📉', label: 'Liabilities' },
        { path: '/upi', icon: '💳', label: 'UPI Transactions' },
        { path: '/goals', icon: '🎯', label: 'Goals' },
    ];

    return (
        <aside className="sidebar">
            <nav className="sidebar-nav">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `sidebar-link ${isActive ? 'active' : ''}`
                        }
                    >
                        <span className="sidebar-icon">{item.icon}</span>
                        <span className="sidebar-label">{item.label}</span>
                    </NavLink>
                ))}
            </nav>
        </aside>
    );
};

export default Sidebar;
