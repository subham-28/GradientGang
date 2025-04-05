import React, { useState } from "react";
import './Navbar.css'
import { Link } from "react-router-dom";
import { assets } from "../../assets/assets";


const Navbar = () => {
    const [menu, setMenu] = useState("home");
  return (
    <nav className='navbar'>
      <div className="logo">  
        <img src={assets.logo} alt="" />
      </div>
      <ul className="nav-links">
        <li onClick={()=>setMenu("home")} className={menu==="home"?"active":""}><Link to="/">Home</Link></li>
        <li onClick={()=>setMenu("convert-units")} className={menu==="convert-units"?"active":""}><Link to="/convert-units">Convert Units</Link></li>
        <li onClick={()=>setMenu("recipe-tips")} className={menu==="recipe-tips"?"active":""}><Link to="/recipe-tips">Recipe Tips</Link></li>
        <li onClick={()=>setMenu("measurement-guide")} className={menu==="measurement-guide"?"active":""}><Link to="/measurement-guide">Measurement Guide</Link></li>
      </ul>
      <div className="auth-buttons">
        <button className="signup">Sign Up</button>
        <button className="login">Login</button>
      </div>
    </nav>
  )
}

export default Navbar
