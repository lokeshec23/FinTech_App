/**
 * Main Layout Component with Navbar and Sidebar
 */
import { Outlet } from 'react-router-dom';
import Navbar from '../common/Navbar';
import Sidebar from '../common/Sidebar';
import './MainLayout.css';

const MainLayout = () => {
    return (
        <div className="main-layout">
            <Navbar />
            <Sidebar />
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default MainLayout;
