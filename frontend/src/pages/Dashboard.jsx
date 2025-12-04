/**
 * Dashboard Page
 */
import { useState, useEffect } from 'react';
import { analyticsAPI, emiAPI } from '../services/api';
import { formatIndianCurrency } from '../utils/formatters';
import { toast } from 'react-toastify';
import { Line, Pie } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import './Dashboard.css';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [upcomingEMIs, setUpcomingEMIs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboardData();
        fetchUpcomingEMIs();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await analyticsAPI.getDashboard();
            setDashboardData(response.data);
        } catch (error) {
            toast.error('Failed to load dashboard data');
        }
        setLoading(false);
    };

    const fetchUpcomingEMIs = async () => {
        try {
            const response = await emiAPI.getUpcoming(7);
            setUpcomingEMIs(response.data);
        } catch (error) {
            console.error('Failed to load upcoming EMIs');
        }
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="loader"></div>
            </div>
        );
    }

    // Prepare chart data
    const spendingTrendData = dashboardData?.spending_trend ? {
        labels: dashboardData.spending_trend.map(item => item.month_name),
        datasets: [
            {
                label: 'Monthly Spending',
                data: dashboardData.spending_trend.map(item => item.total),
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4
            }
        ]
    } : null;

    const categoryData = dashboardData?.category_breakdown ? {
        labels: Object.keys(dashboardData.category_breakdown),
        datasets: [
            {
                data: Object.values(dashboardData.category_breakdown),
                backgroundColor: [
                    '#667eea', '#f093fb', '#4facfe', '#f5576c',
                    '#43e97b', '#fa709a', '#30cfd0', '#a8edea'
                ]
            }
        ]
    } : null;

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#f8fafc'
                }
            }
        },
        scales: {
            x: {
                ticks: { color: '#cbd5e1' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' }
            },
            y: {
                ticks: { color: '#cbd5e1' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' }
            }
        }
    };

    return (
        <div className="dashboard-page">
            <div className="dashboard-header">
                <h1>Dashboard</h1>
                <p className="text-muted">Your financial overview</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-4">
                <div className="stat-card">
                    <div className="stat-label">Total Balance</div>
                    <div className="stat-value">
                        {formatIndianCurrency(dashboardData?.total_balance || 0)}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Total Assets</div>
                    <div className="stat-value">
                        {formatIndianCurrency(dashboardData?.total_assets || 0)}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Total Liabilities</div>
                    <div className="stat-value">
                        {formatIndianCurrency(dashboardData?.total_liabilities || 0)}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Monthly Spending</div>
                    <div className="stat-value">
                        {formatIndianCurrency(dashboardData?.monthly_spending || 0)}
                    </div>
                </div>
            </div>

            {/* Charts */}
            <div className="grid grid-2">
                {spendingTrendData && (
                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Spending Trend</h3>
                        </div>
                        <div className="card-body" style={{ height: '300px' }}>
                            <Line data={spendingTrendData} options={chartOptions} />
                        </div>
                    </div>
                )}

                {categoryData && Object.keys(dashboardData.category_breakdown).length > 0 && (
                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Category Breakdown</h3>
                        </div>
                        <div className="card-body" style={{ height: '300px' }}>
                            <Pie data={categoryData} />
                        </div>
                    </div>
                )}
            </div>

            {/* Financial Metrics */}
            <div className="grid grid-2">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">EMI Burden</h3>
                    </div>
                    <div className="card-body">
                        <div className="metric-value">
                            {dashboardData?.emi_burden_percentage?.toFixed(2) || 0}%
                        </div>
                        <p className="text-muted">of monthly spending</p>
                    </div>
                </div>

                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Asset/Liability Ratio</h3>
                    </div>
                    <div className="card-body">
                        <div className="metric-value">
                            {dashboardData?.asset_liability_ratio?.toFixed(2) || 0}
                        </div>
                        <p className="text-muted">
                            {dashboardData?.asset_liability_ratio > 1 ? 'Healthy' : 'Needs Attention'}
                        </p>
                    </div>
                </div>
            </div>

            {/* Upcoming EMIs */}
            {upcomingEMIs.length > 0 && (
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Upcoming Payments (Next 7 Days)</h3>
                    </div>
                    <div className="card-body">
                        <div className="emi-list">
                            {upcomingEMIs.map((emi) => (
                                <div key={emi.id} className="emi-item">
                                    <div>
                                        <div className="emi-name">{emi.loan_name}</div>
                                        <div className="emi-date text-muted">
                                            Due: {new Date(emi.next_payment_date).toLocaleDateString('en-IN')}
                                        </div>
                                    </div>
                                    <div className="emi-amount">
                                        {formatIndianCurrency(emi.emi_amount)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
