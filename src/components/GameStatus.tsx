import React from 'react';
import './GameStatus.css';

interface GameStatusProps {
  player1Name: string;
  player1HP: number;
  player1MaxHP: number;
  player2Name: string;
  player2HP: number;
  player2MaxHP: number;
  timeLeft: number;
  turnCount: number;
}

export default function GameStatus({
  player1Name,
  player1HP,
  player1MaxHP,
  player2Name,
  player2HP,
  player2MaxHP,
  timeLeft,
  turnCount
}: GameStatusProps) {
  const player1HPPercent = (player1HP / player1MaxHP) * 100;
  const player2HPPercent = (player2HP / player2MaxHP) * 100;

  return (
    <div className="game-status">
      <div className="player-status player1-status">
        <div className="player-name">{player1Name}</div>
        <div className="hp-bar-container">
          <div className="hp-bar">
            <div
              className="hp-fill"
              style={{ width: `${Math.max(0, player1HPPercent)}%` }}
            ></div>
          </div>
          <span className="hp-text">
            {Math.max(0, player1HP)} / {player1MaxHP}
          </span>
        </div>
      </div>

      <div className="center-status">
        <div className="turn-info">
          <div className="timer">
            <span className="timer-label">Time:</span>
            <span className={`timer-value ${timeLeft <= 10 ? 'warning' : ''}`}>
              {timeLeft}s
            </span>
          </div>
          <div className="turn-counter">Turn {turnCount}</div>
        </div>
      </div>

      <div className="player-status player2-status">
        <div className="player-name">{player2Name}</div>
        <div className="hp-bar-container">
          <div className="hp-bar">
            <div
              className="hp-fill"
              style={{ width: `${Math.max(0, player2HPPercent)}%` }}
            ></div>
          </div>
          <span className="hp-text">
            {Math.max(0, player2HP)} / {player2MaxHP}
          </span>
        </div>
      </div>
    </div>
  );
}
