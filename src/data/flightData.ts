// サンプル飛行機データ
export interface FlightData {
  id: string;
  airline: string;
  altitude: number; // メートル
  speed: number; // ノット
  origin: string;
  destination: string;
  aircraft: string;
}

// 世界の主要航空会社サンプルデータ
export const sampleFlights: FlightData[] = [
  // JAL
  { id: 'JAL001', airline: 'JAL', altitude: 10500, speed: 480, origin: 'Tokyo', destination: 'Osaka', aircraft: 'Boeing 787' },
  { id: 'JAL002', airline: 'JAL', altitude: 9800, speed: 470, origin: 'Tokyo', destination: 'Fukuoka', aircraft: 'Airbus A320' },
  { id: 'JAL003', airline: 'JAL', altitude: 11200, speed: 490, origin: 'Osaka', destination: 'Sapporo', aircraft: 'Boeing 787' },

  // ANA
  { id: 'ANA001', airline: 'ANA', altitude: 10800, speed: 485, origin: 'Tokyo', destination: 'Nagoya', aircraft: 'Airbus A350' },
  { id: 'ANA002', airline: 'ANA', altitude: 9500, speed: 465, origin: 'Osaka', destination: 'Tokyo', aircraft: 'Boeing 777' },
  { id: 'ANA003', airline: 'ANA', altitude: 11000, speed: 495, origin: 'Fukuoka', destination: 'Tokyo', aircraft: 'Airbus A320' },

  // International Airlines
  { id: 'UAL001', airline: 'United', altitude: 12200, speed: 500, origin: 'Tokyo', destination: 'San Francisco', aircraft: 'Boeing 787' },
  { id: 'AAL001', airline: 'American', altitude: 11800, speed: 510, origin: 'Osaka', destination: 'Los Angeles', aircraft: 'Boeing 777' },
  { id: 'DAL001', airline: 'Delta', altitude: 12000, speed: 505, origin: 'Tokyo', destination: 'New York', aircraft: 'Airbus A350' },
  { id: 'BAW001', airline: 'British Airways', altitude: 11500, speed: 480, origin: 'Kansai', destination: 'London', aircraft: 'Boeing 787' },
  { id: 'AFR001', airline: 'Air France', altitude: 11900, speed: 495, origin: 'Nagoya', destination: 'Paris', aircraft: 'Airbus A380' },
  { id: 'DLH001', airline: 'Lufthansa', altitude: 12100, speed: 490, origin: 'Tokyo', destination: 'Frankfurt', aircraft: 'Boeing 787' },
  { id: 'KLM001', airline: 'KLM', altitude: 11700, speed: 500, origin: 'Osaka', destination: 'Amsterdam', aircraft: 'Airbus A350' },
  { id: 'CHI001', airline: 'China Airlines', altitude: 10900, speed: 475, origin: 'Tokyo', destination: 'Taipei', aircraft: 'Airbus A350' },
  { id: 'SIA001', airline: 'Singapore Airlines', altitude: 12300, speed: 510, origin: 'Haneda', destination: 'Singapore', aircraft: 'Boeing 787' },
  { id: 'KAL001', airline: 'Korean Air', altitude: 11400, speed: 485, origin: 'Incheon', destination: 'Tokyo', aircraft: 'Boeing 777' },

  // 国内線（短距離）
  { id: 'JDL001', airline: 'JAL', altitude: 7500, speed: 380, origin: 'Haneda', destination: 'Sapporo', aircraft: 'Airbus A320' },
  { id: 'ANA004', airline: 'ANA', altitude: 6800, speed: 360, origin: 'Nagoya', destination: 'Osaka', aircraft: 'Airbus A319' },
  { id: 'SKW001', airline: 'Skymark', altitude: 7200, speed: 370, origin: 'Haneda', destination: 'Fukuoka', aircraft: 'Boeing 737' },
  { id: 'SFJ001', airline: 'StarFlyer', altitude: 8000, speed: 390, origin: 'Tokyo', destination: 'Kitakyushu', aircraft: 'Airbus A320' },
];

// 時系列データ（時間帯別飛行機数）
export const flightCountByHour = [
  { time: '00:00', flights: 45 },
  { time: '01:00', flights: 38 },
  { time: '02:00', flights: 32 },
  { time: '03:00', flights: 28 },
  { time: '04:00', flights: 35 },
  { time: '05:00', flights: 52 },
  { time: '06:00', flights: 78 },
  { time: '07:00', flights: 125 },
  { time: '08:00', flights: 180 },
  { time: '09:00', flights: 210 },
  { time: '10:00', flights: 195 },
  { time: '11:00', flights: 185 },
  { time: '12:00', flights: 220 },
  { time: '13:00', flights: 200 },
  { time: '14:00', flights: 190 },
  { time: '15:00', flights: 210 },
  { time: '16:00', flights: 240 },
  { time: '17:00', flights: 270 },
  { time: '18:00', flights: 285 },
  { time: '19:00', flights: 260 },
  { time: '20:00', flights: 230 },
  { time: '21:00', flights: 200 },
  { time: '22:00', flights: 150 },
  { time: '23:00', flights: 85 },
];

// 航空会社別フライト数
export const flightsByAirline = [
  { name: 'JAL', flights: 3 },
  { name: 'ANA', flights: 3 },
  { name: 'United', flights: 1 },
  { name: 'American', flights: 1 },
  { name: 'Delta', flights: 1 },
  { name: 'British Airways', flights: 1 },
  { name: 'Air France', flights: 1 },
  { name: 'Lufthansa', flights: 1 },
  { name: 'KLM', flights: 1 },
  { name: 'China Airlines', flights: 1 },
  { name: 'Singapore Airlines', flights: 1 },
  { name: 'Korean Air', flights: 1 },
  { name: 'Skymark', flights: 1 },
  { name: 'StarFlyer', flights: 1 },
];
