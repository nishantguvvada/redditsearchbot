"use client"
import { useState, useEffect } from "react";
import toast from 'react-hot-toast';


export const Chat = () => {
    const [userInput, setUserInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [aiResponse, setAIResponse] = useState("");
    const [displayText, setDisplayText] = useState("");
    const [typingIndex, setTypingIndex] = useState(0);
    const [isTyping, setIsTyping] = useState(false);
    const [targetText, setTargetText] = useState("");
    const initialMessage = "Hello, I'm your AI Brand Manager. I analyze your brand's sentiments present in social platforms and news media sources.";

    // Typing effect controller
    useEffect(() => {
        if (isTyping && typingIndex < targetText.length) {
        const timer = setTimeout(() => {
            setDisplayText(prev => prev + targetText[typingIndex]);
            setTypingIndex(prev => prev + 1);
        }, 20);

        return () => clearTimeout(timer);
        } else {
            setIsTyping(false);
        }
    }, [typingIndex, isTyping, targetText]);

    // Handle text updates
    useEffect(() => {
        if (aiResponse) {
            // Start typing AI response
            setTargetText(aiResponse);
            setDisplayText('');
            setTypingIndex(0);
            setIsTyping(true);
        } else {
            // Start typing initial message
            setTargetText(initialMessage);
            setDisplayText('');
            setTypingIndex(0);
            setIsTyping(true);
        }
    }, [aiResponse]);
  
    const askHandler = async () => {
        setIsLoading(true);
        setAIResponse("");
        try {
            if (userInput == "") {
                setIsLoading(false);
                toast.error("No input provided.")
                return
            }

            // const response = await axios.post("http://35.94.209.254:8000/agent", {
            //     user_input: userInput
            // });

            setAIResponse(
                "bubble component is the building block for creating chat interfaces where users can send messages to each other by text, voice notes, images, galleries and other attachments. These components are usually used in chat applications and social media platforms such as Facebook, Twitter/X, WhatsApp, and more."+
                "The examples below provide multiple variations of default, outline, and clean styles coded with the utility classes from Tailwind CSS. Some of the components may require you to include the Flowbite JavaScript to enable the dropdowns and tooltips functionality."
            )

            console.log("response", aiResponse)

            setIsLoading(false);
            toast.success("Response received!")

            // console.log("response:", response);
        } catch(err) {
            console.log("Error: ", err);
            toast.error("Something went wrong.")
            setIsLoading(false);
        }
    }

    return (
        <>
        <div className="mt-12 w-full h-full flex justify-center items-center">
            <div className="h-full w-[50%] border rounded-xl shadow flex flex-col justify-center items-center">
                <div className="pt-8 w-[70%] h-full flex flex-col justify-center items-center ">
                    <p className="pb-8 text-lg font-normal text-gray-500">Try out now!</p>
                    <div className="relative h-96 rounded-lg w-full bg-sky-100 border border-gray-300">
                        {!aiResponse ? 
                            <p className="mx-2 my-2 font-normal text-gray-500 whitespace-pre-wrap">
                            {displayText}
                                {isTyping && (
                                <span className="ml-1 border-r-2 border-black animate-blink"></span>
                                )
                            }
                            </p> : 
                            <p className="mx-2 my-2 font-normal text-gray-500 whitespace-pre-wrap">
                            {displayText}
                                {isTyping && (
                                <span className="ml-1 border-r-2 border-black animate-blink"></span>
                                )
                            }
                            </p>
                                }
                        <textarea onChange={(e) => { setUserInput(userInput => e.target.value )}} id="message" rows="4" className="z-0 absolute bottom-0 block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Analyze your brand image!"></textarea>
                    </div>
                    <button onClick={askHandler} type="button" className="mt-4 mb-4 text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700">Ask</button>
                    <div role="status" className={`absolute ${!isLoading ? "hidden" : ""} -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2`}>
                            <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/></svg>
                            <span className="sr-only">Loading...</span>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}