import React, { useState } from 'react';
import GameScreen from './components/GameScreen';
import StartScreen from './components/StartScreen';
import './App.css';

export default function App() {
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

  return (
    <div className="app">
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
  );
}
