function deleteQuiz(quizId) {
  fetch("/delete-quiz", {
    method: "POST",
    body: JSON.stringify({ quizId: quizId }),
  }).then((_res) => {
    window.location.href = "/display_quiz";
  });
}