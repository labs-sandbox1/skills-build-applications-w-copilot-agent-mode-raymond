import React, { useState, useEffect } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;
      console.log('Fetching activities from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Activities API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Activities data:', activitiesData);
        setActivities(activitiesData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching activities:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) {
    return (
      <div className="content-wrapper">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading activities...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="content-wrapper">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="content-wrapper">
      <h2 className="page-header">
        <i className="bi bi-activity me-2"></i>
        Activity Log
      </h2>
      <div className="table-container">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>User</th>
              <th>Type</th>
              <th>Duration</th>
              <th>Distance</th>
              <th>Calories</th>
              <th>Points</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity) => (
              <tr key={activity.id}>
                <td>
                  <strong>{activity.user_name || activity.user}</strong>
                </td>
                <td>
                  <span className="badge bg-info">{activity.activity_type}</span>
                </td>
                <td>{activity.duration_minutes} min</td>
                <td>{activity.distance_km} km</td>
                <td>{activity.calories_burned} cal</td>
                <td>
                  <span className="badge bg-success">{activity.points_earned} pts</span>
                </td>
                <td>{new Date(activity.date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-3 text-muted">
        <small>Total Activities: {activities.length}</small>
      </div>
    </div>
  );
};

export default Activities;
