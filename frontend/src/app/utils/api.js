"use client"

import axios from "axios";

export const fetchAnswer = async (question) => {
  try {
    const res = await axios.post("http://127.0.0.1:8000/chat/", {query: question });
    console.log(res.data.answer);
    return res.data.answer;
  } catch (error) {
    return "Error fetching answer.";
  }
};
