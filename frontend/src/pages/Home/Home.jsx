import React from 'react'
import './Home.css'
import Hero from '../../components/Hero/Hero'
import Slogan from '../../components/Slogan/Slogan'
import About from '../../components/About/About'

const Home = () => {
  return (
    <div>
      <Hero />
      <Slogan />
      <About />
    </div>
  )
}

export default Home
