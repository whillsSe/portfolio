// src/components/Navigation.js
import React from 'react';
import { useLocation,NavLink,matchPath } from 'react-router-dom';
import './style.css';
import icon_home from '../../icons/house-solid.svg';
import icon_cal from '../../icons/calendar-regular.svg';
import icon_jedi from '../../icons/jedi-order.svg';

function Navigator() {
  const location = useLocation();
  const isSecondWindowActive = !location.pathname.startsWith('/task');
  function NavIcon({title,src}){
    return(
      <div className='navigation_button'>
        <img src={src}></img>
        <p>{title}</p>
      </div>
    )
  }
  return (
    <div className={`navigation ${isSecondWindowActive ? 'top' : 'bottom'}`}>
      {isSecondWindowActive ?
            <nav>
              <NavLink to="/home" ><NavIcon title='Home' src={icon_home}/></NavLink>
              <NavLink to="/calendar"><NavIcon title='Calendar' src={icon_cal}/></NavLink>
              <button>Add New</button>
              <NavLink to="/view-tasks"><NavIcon title='Tasks' src={icon_jedi}/></NavLink>
              <NavLink to="/account">Account</NavLink>
            </nav>
        :
            <button>Back to prev</button>
        }
    </div>
  );
}
export default Navigator;

