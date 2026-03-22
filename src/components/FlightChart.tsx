import React, { useState } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  sampleFlights,
  flightCountByHour,
  flightsByAirline,
} from '../data/flightData';
import '../styles/FlightChart.css';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#a4de6c', '#d084d0'];

export const FlightChart: React.FC = () => {
  const [selectedView, setSelectedView] = useState('timeline');

  // 高度分布データ
  const altitudeDistribution = [
    { range: '6000-8000m', count: 4 },
    { range: '8000-10000m', count: 3 },
    { range: '10000-12000m', count: 15 },
    { range: '12000m+', count: 3 },
  ];

  // 速度分布データ
  const speedDistribution = [
    { range: '350-400kt', count: 4 },
    { range: '400-450kt', count: 6 },
    { range: '450-500kt', count: 12 },
    { range: '500kt+', count: 3 },
  ];

  return (
    <div className="flight-chart-container">
      <header className="flight-header">
        <h1>✈️ Flight Data Viewer</h1>
        <p>World Flight Status</p>
      </header>

      <nav className="view-selector">
        <button
          className={selectedView === 'timeline' ? 'active' : ''}
          onClick={() => setSelectedView('timeline')}
        >
          Timeline
        </button>
        <button
          className={selectedView === 'airlines' ? 'active' : ''}
          onClick={() => setSelectedView('airlines')}
        >
          Airlines
        </button>
        <button
          className={selectedView === 'altitude' ? 'active' : ''}
          onClick={() => setSelectedView('altitude')}
        >
          Altitude
        </button>
        <button
          className={selectedView === 'speed' ? 'active' : ''}
          onClick={() => setSelectedView('speed')}
        >
          Speed
        </button>
        <button
          className={selectedView === 'list' ? 'active' : ''}
          onClick={() => setSelectedView('list')}
        >
          List
        </button>
      </nav>

      <main className="chart-main">
        {selectedView === 'timeline' && (
          <div className="chart-section">
            <h2>Flights by Hour</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={flightCountByHour}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="time"
                  tick={{ fontSize: 12 }}
                  interval={2}
                />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="flights"
                  stroke="#8884d8"
                  dot={false}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedView === 'airlines' && (
          <div className="chart-section">
            <h2>Flights by Airline</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={flightsByAirline}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} angle={-45} textAnchor="end" height={80} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="flights" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedView === 'altitude' && (
          <div className="chart-section">
            <h2>Altitude Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={altitudeDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedView === 'speed' && (
          <div className="chart-section">
            <h2>Speed Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={speedDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, count }) => `${name}: ${count}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {speedDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedView === 'list' && (
          <div className="chart-section">
            <h2>Active Flights ({sampleFlights.length})</h2>
            <div className="flights-list">
              {sampleFlights.map((flight) => (
                <div key={flight.id} className="flight-item">
                  <div className="flight-header-info">
                    <span className="airline">{flight.airline}</span>
                    <span className="flight-id">{flight.id}</span>
                  </div>
                  <div className="flight-route">
                    {flight.origin} → {flight.destination}
                  </div>
                  <div className="flight-details">
                    <span>✈️ {flight.aircraft}</span>
                    <span>📏 {flight.altitude.toLocaleString()}m</span>
                    <span>🚀 {flight.speed}kt</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="flight-footer">
        <p>Total Active Flights: {sampleFlights.length}</p>
        <p>Data Updated: Sample Data</p>
      </footer>
    </div>
  );
};
