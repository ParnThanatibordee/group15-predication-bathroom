import './App.css';
import AboutusPopUp from './components/AboutusPopUp';
import Room from './components/Room';
import React, { useState, useEffect } from 'react';
import AboutUsData from './components/AboutUsData';
import axios from 'axios';

function App() {

  const [buttonPopup, setButtonPopup] = useState(false);
  const [roomData, setRoomData] = useState()

  useEffect(() => {
    setInterval(getData, 1000)
  }, [])

  const fetchData = async () => {
    const { data } = await axios.get("https://randomuser.me/api/")
    console.log(data)
  }

  const getData = async () => {
    const response = await axios.get("data.json")
    setRoomData(response.data)
  }

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Restroom Time Estimate
        </p>
      </header>
      {roomData ? <div>
        <div className="estimate-time">
          <p>ห้องน้ำจะว่างในอีกประมาณ {parseInt(roomData.estimatedTime / 60)}:{parseInt(roomData.estimatedTime % 60) > 10 ? '' : '0'}{parseInt(roomData.estimatedTime % 60)} นาที</p>
        </div>
        <div className='restroom-list'>
          {roomData.room.map(r =>
            (<div className="restroom-card"><Room room={r} /></div>))}
        </div>
      </div> : <div>Loading...</div>}
      <footer className="foot" style={{ padding: '10px 0px' }}>
        <button className="about-us" onClick={() => setButtonPopup(true)}>About us</button>
        <AboutusPopUp trigger={buttonPopup} closePopup={() => setButtonPopup(false)} className="about-us">
          <AboutUsData />
          <div className="popupheader">
            <p onClick={() => setButtonPopup(false)} className="button-84">Close</p>
          </div>
        </AboutusPopUp>
        <a href="https://github.com/ParnThanatibordee/group15-predication-bathroom" className="git-repo">
          Github
        </a>
      </footer>
    </div>
  );
}

export default App;
