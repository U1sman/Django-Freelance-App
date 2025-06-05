import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass, faBell } from '@fortawesome/free-solid-svg-icons'
import styles from './Navbar.module.css'

const Navbar = () => {
  return (
    <>
    <div className={styles.navbarContainer}>
      <h1>Freelance App</h1>
      <div className="searchBarContainer">
          <input type="text" className='searchBar' placeholder='What service are you looking for today?' />
          <FontAwesomeIcon icon={faMagnifyingGlass} />
      </div>
      <div className="notificationsIcon">
          <FontAwesomeIcon icon={faBell} />
      </div>
      <div className="profileIcon">
          profilepic
      </div>
    </div>
    </>
  )
}

export default Navbar