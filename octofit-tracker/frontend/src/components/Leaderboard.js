import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
      console.log('Fetching leaderboard from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Leaderboard API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard data:', leaderboardData);
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="content-wrapper">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading leaderboard...</p>
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
        <i className="bi bi-trophy me-2"></i>
        Leaderboard
      </h2>
      <div className="table-container">
        <table className="table table-hover">
          <thead>
            <tr>
              <th style={{width: '80px'}}>Rank</th>
              <th>User</th>
              <th>Total Points</th>
              <th>Activities</th>
              <th>Teams</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry.id || index} className={index < 3 ? 'table-warning' : ''}>
                <td>
                  <span className="rank-badge">
                    {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1}
                  </span>
                </td>
                <td>
                  <strong>{entry.username}</strong>
                </td>
                <td>
                  <span className="points-display">{entry.total_points}</span>
                </td>
                <td>
                  <span className="badge bg-info">{entry.activity_count || 0}</span>
                </td>
                <td>
                  {entry.teams && entry.teams.length > 0 ? (
                    entry.teams.map((team, idx) => (
                      <span key={idx} className="badge bg-secondary me-1">{team}</span>
                    ))
                  ) : (
                    <span className="text-muted">No teams</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-3 text-muted">
        <small>Total Competitors: {leaderboard.length}</small>
      </div>
    </div>
  );
};

export default Leaderboard;
