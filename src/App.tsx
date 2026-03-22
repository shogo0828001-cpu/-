import React, { useState } from 'react';
import GameScreen from './components/GameScreen';
import StartScreen from './components/StartScreen';
import { FlightChart } from './components/FlightChart';
import './App.css';

export default function App() {
  const [appMode, setAppMode] = useState<'menu' | 'game' | 'flight'>('menu');
  const [gameState, setGameState] = useState<'start' | 'playing' | 'gameOver'>('start');
  const [player1Name, setPlayer1Name] = useState('Player 1');
  const [player2Name, setPlayer2Name] = useState('Player 2');
  const [gameKey, setGameKey] = useState(0);

  const handleGameStart = (name1: string, name2: string) => {
    setPlayer1Name(name1 || 'Player 1');
    setPlayer2Name(name2 || 'Player 2');
    setGameState('playing');
    setGameKey(prev => prev + 1);
  };

  const handleGameEnd = () => {
    setGameState('gameOver');
  };

  const handleReturnToStart = () => {
    setGameState('start');
  };

  const handleReturnToMenu = () => {
    setAppMode('menu');
  };

  return (
    <div className="app">
      {appMode === 'menu' && (
        <div className="main-menu">
          <div className="menu-content">
            <h1>Welcome</h1>
            <div className="menu-buttons">
              <button
                className="menu-btn game-btn"
                onClick={() => {
                  setAppMode('game');
                  setGameState('start');
                }}
              >
                🎮 Grave Cross Game
              </button>
              <button
                className="menu-btn flight-btn"
                onClick={() => setAppMode('flight')}
              >
                ✈️ Flight Viewer
              </button>
            </div>
          </div>
        </div>
      )}

      {appMode === 'game' && (
        <div>
          <button className="back-btn" onClick={handleReturnToMenu}>← Back to Menu</button>
          {gameState === 'start' && (
            <StartScreen onStartGame={handleGameStart} />
          )}
          {gameState === 'playing' && (
            <GameScreen
              key={gameKey}
              player1Name={player1Name}
              player2Name={player2Name}
              onGameEnd={handleGameEnd}
              onReturnToStart={handleReturnToStart}
            />
          )}
        </div>
      )}

      {appMode === 'flight' && (
        <div>
          <button className="back-btn" onClick={handleReturnToMenu}>← Back to Menu</button>
          <FlightChart />
        </div>
      )}
    </div>
  );
}
