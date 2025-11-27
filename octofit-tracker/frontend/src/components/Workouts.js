import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
      console.log('Fetching workouts from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Workouts API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts data:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="content-wrapper">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading workouts...</p>
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

  const getDifficultyBadge = (level) => {
    const badges = {
      'Beginner': 'success',
      'Intermediate': 'warning',
      'Advanced': 'danger'
    };
    return badges[level] || 'secondary';
  };

  return (
    <div className="content-wrapper">
      <h2 className="page-header">
        <i className="bi bi-lightning me-2"></i>
        Workout Suggestions
      </h2>
      <div className="row">
        {workouts.map((workout) => (
          <div key={workout.id} className="col-lg-6 col-md-12 mb-4">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title text-white mb-0">{workout.name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text text-muted mb-3">{workout.description}</p>
                <div className="row g-2 mb-3">
                  <div className="col-6">
                    <div className="p-3 bg-light rounded">
                      <small className="text-muted d-block">Category</small>
                      <strong>{workout.category}</strong>
                    </div>
                  </div>
                  <div className="col-6">
                    <div className="p-3 bg-light rounded">
                      <small className="text-muted d-block">Difficulty</small>
                      <span className={`badge bg-${getDifficultyBadge(workout.difficulty_level)}`}>
                        {workout.difficulty_level}
                      </span>
                    </div>
                  </div>
                  <div className="col-6">
                    <div className="p-3 bg-light rounded">
                      <small className="text-muted d-block">Duration</small>
                      <strong>{workout.duration_minutes} min</strong>
                    </div>
                  </div>
                  <div className="col-6">
                    <div className="p-3 bg-light rounded">
                      <small className="text-muted d-block">Calories</small>
                      <strong>{workout.estimated_calories} cal</strong>
                    </div>
                  </div>
                </div>
                {workout.equipment_needed && (
                  <div className="alert alert-info mb-0">
                    <strong>Equipment:</strong> {workout.equipment_needed}
                  </div>
                )}
              </div>
              <div className="card-footer bg-transparent">
                <button className="btn btn-primary w-100">Start Workout</button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-3 text-muted">
        <small>Total Workouts: {workouts.length}</small>
      </div>
    </div>
  );
};

export default Workouts;
