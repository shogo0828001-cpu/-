import React from 'react';
import { GameResult } from '../game/gameLogic';
import './TurnResult.css';

interface TurnResultProps {
  result: GameResult;
  onContinue: () => void;
}

export default function TurnResult({ result, onContinue }: TurnResultProps) {
  const isWin = result.winner !== 'draw';
  const emojis = {
    player1: '🎯',
    player2: '🎯',
    draw: '⚡'
  };

  return (
    <div className="turn-result-overlay">
      <div className={`turn-result ${result.winner}`}>
        <div className="result-emoji">{emojis[result.winner]}</div>
        <div className="result-title">
          {result.winner === 'draw' ? 'Draw!' : 'Hit!'}
        </div>
        <div className="result-description">{result.description}</div>
        {isWin && <div className="damage-display">💥 {result.damage} Damage 💥</div>}
        <button className="continue-button" onClick={onContinue}>
          Continue
        </button>
      </div>
    </div>
  );
}
