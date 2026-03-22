import React from 'react';
import { Hand } from '../game/gameLogic';
import './HandSelector.css';

interface HandSelectorProps {
  onHandSelected: (hand: Hand) => void;
  selectedHand: Hand | null;
  disabled: boolean;
}

export default function HandSelector({
  onHandSelected,
  selectedHand,
  disabled
}: HandSelectorProps) {
  const hands: Array<{ type: Hand; emoji: string; label: string }> = [
    { type: 'rock', emoji: '✊', label: 'Rock' },
    { type: 'scissors', emoji: '✌️', label: 'Scissors' },
    { type: 'paper', emoji: '✋', label: 'Paper' }
  ];

  return (
    <div className="hand-selector">
      <h3>Choose your hand:</h3>
      <div className="hands-container">
        {hands.map((hand) => (
          <button
            key={hand.type}
            className={`hand-button ${selectedHand === hand.type ? 'selected' : ''}`}
            onClick={() => onHandSelected(hand.type)}
            disabled={disabled}
            title={hand.label}
          >
            <span className="hand-emoji">{hand.emoji}</span>
            <span className="hand-label">{hand.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
