export default function AnswerBox({ answer }) {
    return (
      <div className="bg-gray-700 text-white rounded-lg p-4">
        <p>{answer}</p>
      </div>
    );
  }