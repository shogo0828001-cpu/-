import React, { useState, useEffect } from 'react';
import { cards } from '../data/cards';
import { determineWinner, Hand } from '../game/gameLogic';
import CardSelector from './CardSelector';
import HandSelector from './HandSelector';
import GameStatus from './GameStatus';
import TurnResult from './TurnResult';
import './GameScreen.css';

interface GameScreenProps {
  player1Name: string;
  player2Name: string;
  onGameEnd: () => void;
  onReturnToStart: () => void;
}

interface PlayerState {
  selectedCards: string[];
  currentHP: number;
  totalHP: number;
}

export default function GameScreen({
  player1Name,
  player2Name,
  onGameEnd,
  onReturnToStart
}: GameScreenProps) {
  const [player1, setPlayer1] = useState<PlayerState>({
    selectedCards: [cards[0].id, cards[1].id, cards[2].id],
    currentHP: cards[0].hp + cards[1].hp + cards[2].hp,
    totalHP: cards[0].hp + cards[1].hp + cards[2].hp
  });

  const [player2, setPlayer2] = useState<PlayerState>({
    selectedCards: [cards[5].id, cards[6].id, cards[7].id],
    currentHP: cards[5].hp + cards[6].hp + cards[7].hp,
    totalHP: cards[5].hp + cards[6].hp + cards[7].hp
  });

  const [player1Hand, setPlayer1Hand] = useState<Hand | null>(null);
  const [player2Hand, setPlayer2Hand] = useState<Hand | null>(null);
  const [timeLeft, setTimeLeft] = useState(60);
  const [turnCount, setTurnCount] = useState(0);
  const [lastResult, setLastResult] = useState<any>(null);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);
  const [showResult, setShowResult] = useState(false);

  // Timer for turns
  useEffect(() => {
    if (gameOver || timeLeft === 0) return;

    const interval = setInterval(() => {
      setTimeLeft(prev => {
        if (prev === 1) {
          handleTurnEnd();
          return 60;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [gameOver, timeLeft]);

  // Check for game over
  useEffect(() => {
    if (player1.currentHP <= 0) {
      setGameOver(true);
      setWinner(player2Name);
    } else if (player2.currentHP <= 0) {
      setGameOver(true);
      setWinner(player1Name);
    }
  }, [player1.currentHP, player2.currentHP, player1Name, player2Name]);

  const handleTurnEnd = () => {
    if (!player1Hand || !player2Hand) return;

    const player1Card = cards.find(c => c.id === player1.selectedCards[0])!;
    const player2Card = cards.find(c => c.id === player2.selectedCards[0])!;

    const result = determineWinner(
      player1Hand,
      player2Hand,
      {
        damageToRock: player1Card.damageToRock,
        damageToScissors: player1Card.damageToScissors,
        damageToPaper: player1Card.damageToPaper
      },
      {
        damageToRock: player2Card.damageToRock,
        damageToScissors: player2Card.damageToScissors,
        damageToPaper: player2Card.damageToPaper
      }
    );

    setLastResult(result);
    setShowResult(true);

    // Update HP
    if (result.winner === 'player1') {
      setPlayer2(prev => ({
        ...prev,
        currentHP: Math.max(0, prev.currentHP - result.damage)
      }));
    } else if (result.winner === 'player2') {
      setPlayer1(prev => ({
        ...prev,
        currentHP: Math.max(0, prev.currentHP - result.damage)
      }));
    }

    setTurnCount(prev => prev + 1);
    setPlayer1Hand(null);
    setPlayer2Hand(null);
  };

  const handleContinue = () => {
    setShowResult(false);
  };

  const handleQuit = () => {
    onReturnToStart();
  };

  const player1CardData = player1.selectedCards.map(id => cards.find(c => c.id === id)!);
  const player2CardData = player2.selectedCards.map(id => cards.find(c => c.id === id)!);

  if (gameOver) {
    return (
      <div className="game-screen">
        <div className="game-over">
          <h1>Game Over!</h1>
          <h2 className="winner-text">🏆 {winner} Wins! 🏆</h2>
          <p className="turn-count">Battle lasted {turnCount} turns</p>
          <button onClick={handleQuit} className="play-again-btn">
            Return to Menu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="game-screen">
      <GameStatus
        player1Name={player1Name}
        player1HP={player1.currentHP}
        player1MaxHP={player1.totalHP}
        player2Name={player2Name}
        player2HP={player2.currentHP}
        player2MaxHP={player2.totalHP}
        timeLeft={timeLeft}
        turnCount={turnCount}
      />

      <div className="game-content">
        <div className="player-section player1-section">
          <h2>{player1Name}</h2>
          <CardSelector
            cards={player1CardData}
            onSelectCards={(newCards) =>
              setPlayer1(prev => ({
                ...prev,
                selectedCards: newCards
              }))
            }
            selectedCards={player1.selectedCards}
          />
          <HandSelector
            onHandSelected={(hand) => setPlayer1Hand(hand)}
            selectedHand={player1Hand}
            disabled={showResult}
          />
        </div>

        <div className="vs-section">VS</div>

        <div className="player-section player2-section">
          <h2>{player2Name}</h2>
          <CardSelector
            cards={player2CardData}
            onSelectCards={(newCards) =>
              setPlayer2(prev => ({
                ...prev,
                selectedCards: newCards
              }))
            }
            selectedCards={player2.selectedCards}
          />
          <HandSelector
            onHandSelected={(hand) => setPlayer2Hand(hand)}
            selectedHand={player2Hand}
            disabled={showResult}
          />
        </div>
      </div>

      {showResult && lastResult && (
        <TurnResult result={lastResult} onContinue={handleContinue} />
      )}

      {!showResult && player1Hand && player2Hand && (
        <div className="ready-notice">
          Both players ready! Waiting for turn to end ({timeLeft}s)...
        </div>
      )}
    </div>
  );
}
