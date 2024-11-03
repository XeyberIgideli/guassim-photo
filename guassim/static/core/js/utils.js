const getLanguageFromCookie = () => {
	const cookies = document.cookie.split('; ');
	const languageCookie = cookies.find(cookie => cookie.startsWith("django_language"));
	return languageCookie ? languageCookie.split('=')[1] : ''; 
};

function generateGuid() {
	return Math.random().toString(36).substring(2, 15) +
		Math.random().toString(36).substring(2, 15);
}
  

const language = getLanguageFromCookie();