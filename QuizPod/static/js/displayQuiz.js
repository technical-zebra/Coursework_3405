/**
 * The function sends a POST request to delete a quiz and redirects to the display quiz page.
 * @param quizId - The quizId parameter is a unique identifier for a quiz that is being passed as an
 * argument to the deleteQuiz function. It is used to specify which quiz should be deleted when the
 * function is called.
 */
function deleteQuiz(quizId) {
  fetch("/delete-quiz", {
    method: "POST",
    body: JSON.stringify({ quizId: quizId }),
  }).then((_res) => {
    window.location.href = "/display_quiz";
  });
}