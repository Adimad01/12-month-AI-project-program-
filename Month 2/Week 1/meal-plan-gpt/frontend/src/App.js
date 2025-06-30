import React, { useState } from 'react';
import './App.css';

function App() {
  const [diet, setDiet] = useState('');
  const [calories, setCalories] = useState('');
  const [days, setDays] = useState(7);
  const [plan, setPlan] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    setPlan([]);
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ diet, calories: parseInt(calories), days: parseInt(days) })
      });

      const data = await response.json();

      // Vérifie si c’est un tableau de jours (plan généré)
      if (Array.isArray(data)) {
        setPlan(data);
      } else {
        setError(data.detail || 'Erreur pendant la génération.');
      }
    } catch (err) {
      console.error(err);
      setError('Erreur de connexion avec le backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="wrapper">
      <h1>🍽️ Meal Plan GPT</h1>
      <div className="card">
        <div className="form-group">
          <label>Diet type</label>
          <input type="text" value={diet} onChange={e => setDiet(e.target.value)} placeholder="e.g. vegan, keto" />
        </div>
        <div className="form-group">
          <label>Calories per day</label>
          <input type="number" value={calories} onChange={e => setCalories(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Number of days</label>
          <input type="number" value={days} onChange={e => setDays(e.target.value)} />
        </div>
        <button onClick={handleGenerate} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Plan'}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      <div className="plan-container">
        {plan.map((day) => (
          <div className="day-card" key={day.day}>
            <h2>Day {day.day}</h2>
            <ul>
              <li><strong>Breakfast:</strong> {day.meals.breakfast}</li>
              <li><strong>Lunch:</strong> {day.meals.lunch}</li>
              <li><strong>Dinner:</strong> {day.meals.dinner}</li>
              <li><strong>Snack:</strong> {day.meals.snack}</li>
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
