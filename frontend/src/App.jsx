import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home/Home";
import Converter from "./pages/Converter/Converter";
import Navbar from "./components/Navbar/Navbar";
import Footer from "./components/Footer/Footer";
import './index.css';

function App() {
  return (
    <>
      <Navbar />
      <div className="app">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/convert-units" element={<Converter/>} />
        </Routes>
      </div>
      <Footer />
    </>
  );
}

export default App;
