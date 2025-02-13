import { Navbar } from "../../components/Navbar";
import { Hero } from "../../components/Hero";
import { Chat } from "../../components/Chat";
import { Footer } from "../../components/Footer";
import { Toaster } from "react-hot-toast";
import { Test } from "../../components/Test";

export default function Home() {
  return (
    <>
      <Navbar/>
      <Hero/>
      <Chat/>
      <Test/>
      <Footer/>
      <Toaster/>
    </>
  );
}
