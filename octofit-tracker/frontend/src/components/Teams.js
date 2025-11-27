import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
      console.log('Fetching teams from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Teams API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams data:', teamsData);
        setTeams(teamsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching teams:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) {
    return (
      <div className="content-wrapper">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading teams...</p>
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
        <i className="bi bi-people me-2"></i>
        Teams
      </h2>
      <div className="row">
        {teams.map((team) => (
          <div key={team.id} className="col-lg-4 col-md-6 mb-4">
            <div className="card h-100">
              <div className="card-header">
                <h5 className="card-title text-white mb-0">{team.name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text text-muted">{team.description}</p>
                <hr />
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <span className="text-muted">Total Points:</span>
                  <span className="badge bg-primary fs-6">{team.total_points}</span>
                </div>
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <span className="text-muted">Members:</span>
                  <span className="badge bg-secondary">{team.member_count || 0}</span>
                </div>
                <div className="d-flex justify-content-between align-items-center">
                  <span className="text-muted">Created:</span>
                  <small>{new Date(team.created_at).toLocaleDateString()}</small>
                </div>
              </div>
              <div className="card-footer bg-transparent">
                <button className="btn btn-outline-primary btn-sm w-100">View Details</button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-3 text-muted">
        <small>Total Teams: {teams.length}</small>
      </div>
    </div>
  );
};

export default Teams;
