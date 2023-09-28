// src/components/App.js
import React from 'react';
import {Routes, Route} from 'react-router-dom';
import Home from './contentArea/Home';
import Calendar from './contentArea/Calendar';
import ViewTasks from './contentArea/ViewTasks';
import Profile from './contentArea/Profile';
import  SecondWindow  from './secondWindow/SecondWindow';
import Navigator from './navigation/Navigator';
function App() {
  return (
      <div>
        <Navigator></Navigator>
        <Routes>
          <Route path="/home" element={ <Home/> } />
          <Route path="/calendar" element={<Calendar/>} />
          <Route path="/view-tasks" element={<ViewTasks/>} />
          <Route path="/account" element={<Profile/>} />
          <Route path="/task/:taskId/edit" element={<SecondWindow/>} />
          <Route path="/task/create" element={<SecondWindow/>} />
          <Route path="/task/:taskId" element={<SecondWindow/>} />
        </Routes>
      </div>
  );
}

export default App;
