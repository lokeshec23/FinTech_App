/**
 * Assets Management Page
 */
import { useState, useEffect } from 'react';
import { assetAPI } from '../services/api';
import { formatIndianCurrency, formatDate } from '../utils/formatters';
import { toast } from 'react-toastify';
import '../pages/Expenses.css';

const Assets = () => {
    const [assets, setAssets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editingAsset, setEditingAsset] = useState(null);
    const [formData, setFormData] = useState({
        asset_type: 'Property',
        name: '',
        current_value: '',
        purchase_value: '',
        purchase_date: '',
        description: ''
    });

    const assetTypes = ['Property', 'Vehicle', 'Investment', 'Jewelry', 'Electronics', 'Others'];

    useEffect(() => {
        fetchAssets();
    }, []);

    const fetchAssets = async () => {
        try {
            const response = await assetAPI.getAll();
            setAssets(response.data);
        } catch (error) {
            toast.error('Failed to load assets');
        }
        setLoading(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                asset_type: formData.asset_type,
                name: formData.name,
                current_value: parseFloat(formData.current_value),
                purchase_value: formData.purchase_value ? parseFloat(formData.purchase_value) : null,
                purchase_date: formData.purchase_date || null,
                description: formData.description || null
            };

            if (editingAsset) {
                await assetAPI.update(editingAsset.id, data);
                toast.success('Asset updated successfully');
            } else {
                await assetAPI.create(data);
                toast.success('Asset added successfully');
            }

            setShowModal(false);
            setEditingAsset(null);
            resetForm();
            fetchAssets();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Failed to save asset');
        }
    };

    const handleEdit = (asset) => {
        setEditingAsset(asset);
        setFormData({
            asset_type: asset.asset_type,
            name: asset.name,
            current_value: asset.current_value.toString(),
            purchase_value: asset.purchase_value?.toString() || '',
            purchase_date: asset.purchase_date || '',
            description: asset.description || ''
        });
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this asset?')) return;

        try {
            await assetAPI.delete(id);
            toast.success('Asset deleted successfully');
            fetchAssets();
        } catch (error) {
            toast.error('Failed to delete asset');
        }
    };

    const resetForm = () => {
        setFormData({
            asset_type: 'Property',
            name: '',
            current_value: '',
            purchase_value: '',
            purchase_date: '',
            description: ''
        });
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setEditingAsset(null);
        resetForm();
    };

    if (loading) {
        return <div className="loading-container"><div className="loader"></div></div>;
    }

    return (
        <div className="expenses-page">
            <div className="page-header">
                <div>
                    <h1>Assets</h1>
                    <p className="text-muted">Track your valuable assets</p>
                </div>
                <button onClick={() => setShowModal(true)} className="btn btn-primary">
                    + Add Asset
                </button>
            </div>

            <div className="expenses-grid">
                {assets.length === 0 ? (
                    <div className="empty-state">
                        <p>No assets found. Add your first asset to get started!</p>
                    </div>
                ) : (
                    assets.map((asset) => (
                        <div key={asset.id} className="expense-card">
                            <div className="expense-header">
                                <span className="expense-category">{asset.asset_type}</span>
                                <span className="expense-amount">{formatIndianCurrency(asset.current_value)}</span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{asset.name}</h3>
                            <p className="expense-description">{asset.description || 'No description'}</p>
                            <div className="expense-footer">
                                <div className="expense-meta">
                                    {asset.purchase_date && <span>{formatDate(asset.purchase_date)}</span>}
                                    {asset.purchase_value && (
                                        <span className="expense-method">
                                            Bought: {formatIndianCurrency(asset.purchase_value)}
                                        </span>
                                    )}
                                </div>
                                <div className="expense-actions">
                                    <button onClick={() => handleEdit(asset)} className="btn-icon">✏️</button>
                                    <button onClick={() => handleDelete(asset.id)} className="btn-icon btn-danger">🗑️</button>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {showModal && (
                <div className="modal-overlay" onClick={handleCloseModal}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>{editingAsset ? 'Edit Asset' : 'Add Asset'}</h2>
                            <button onClick={handleCloseModal} className="modal-close">×</button>
                        </div>

                        <form onSubmit={handleSubmit} className="modal-form">
                            <div className="input-group">
                                <label className="input-label">Asset Type</label>
                                <select
                                    className="input"
                                    value={formData.asset_type}
                                    onChange={(e) => setFormData({ ...formData, asset_type: e.target.value })}
                                    required
                                >
                                    {assetTypes.map(type => (
                                        <option key={type} value={type}>{type}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="input-group">
                                <label className="input-label">Name</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    placeholder="e.g., Mumbai Apartment"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Current Value (₹)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.current_value}
                                    onChange={(e) => setFormData({ ...formData, current_value: e.target.value })}
                                    placeholder="0.00"
                                    step="0.01"
                                    min="0"
                                    required
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Purchase Value (₹) - Optional</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.purchase_value}
                                    onChange={(e) => setFormData({ ...formData, purchase_value: e.target.value })}
                                    placeholder="0.00"
                                    step="0.01"
                                    min="0"
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Purchase Date - Optional</label>
                                <input
                                    type="date"
                                    className="input"
                                    value={formData.purchase_date}
                                    onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })}
                                />
                            </div>

                            <div className="input-group">
                                <label className="input-label">Description - Optional</label>
                                <textarea
                                    className="input"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    placeholder="Additional details..."
                                    rows="3"
                                />
                            </div>

                            <div className="modal-actions">
                                <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    {editingAsset ? 'Update' : 'Add'} Asset
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Assets;
