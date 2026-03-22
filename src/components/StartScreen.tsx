import React, { useState } from 'react';
import './StartScreen.css';

interface StartScreenProps {
  onStartGame: (player1Name: string, player2Name: string) => void;
}

export default function StartScreen({ onStartGame }: StartScreenProps) {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');

  const handleStart = () => {
    onStartGame(player1, player2);
  };

  return (
    <div className="start-screen">
      <div className="start-container">
        <h1 className="start-title">⚔️ Grave Cross ⚔️</h1>
        <p className="start-subtitle">A Strategic Card Battle Game</p>

        <div className="input-group">
          <label htmlFor="player1">Player 1 Name:</label>
          <input
            id="player1"
            type="text"
            value={player1}
            onChange={(e) => setPlayer1(e.target.value)}
            placeholder="Enter name (or leave blank)"
            maxLength={20}
            onKeyPress={(e) => e.key === 'Enter' && handleStart()}
          />
        </div>

        <div className="input-group">
          <label htmlFor="player2">Player 2 Name:</label>
          <input
            id="player2"
            type="text"
            value={player2}
            onChange={(e) => setPlayer2(e.target.value)}
            placeholder="Enter name (or leave blank)"
            maxLength={20}
            onKeyPress={(e) => e.key === 'Enter' && handleStart()}
          />
        </div>

        <button className="start-button" onClick={handleStart}>
          Start Game
        </button>

        <div className="rules">
          <h3>How to Play:</h3>
          <ul>
            <li>Each player has 3 cards with HP values</li>
            <li>Every turn (1 minute), choose a hand: Rock, Paper, or Scissors</li>
            <li>Win the hand to deal damage to opponent</li>
            <li>Damage amount depends on your card's attack power</li>
            <li>First to reduce opponent's HP to 0 wins!</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
