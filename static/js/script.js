const animeData = {
  bleach: {
    titleImg: "images/movies/bleach_title.png",
    year: "2012",
    rating: "3+",
    seasons: "17+ Seasons",
    genres: "Action, Adventure",
    description: "Bleach follows Ichigo Kurosaki, a Soul Reaper battling evil spirits known as Hollows.",
    trailer: "https://www.youtube.com/watch?v=78WIYzX_m98"
  },
  onepiece: {
    titleImg: "images/movies/onepiece_title.png",
    year: "1999",
    rating: "7+",
    seasons: "20+ Seasons",
    genres: "Adventure, Fantasy",
    description: "One Piece follows Luffy and his crew on their quest for the legendary treasure.",
    trailer: "https://www.youtube.com/watch?v=MCb13f1c7EI"
  },
  hunterxhunter: {
    titleImg: "images/movies/hunter_title.png",
    year: "2011",
    rating: "12+",
    seasons: "6 Seasons",
    genres: "Action, Fantasy",
    description: "Hunter x Hunter follows Gon Freecss as he trains to become a Hunter and find his father.",
    trailer: "https://www.youtube.com/watch?v=d6kBeJjTGnY"
  },
  demonslayer: {
    titleImg: "images/movies/demon_title.png",
    year: "2019",
    rating: "16+",
    seasons: "4 Seasons",
    genres: "Action, Supernatural",
    description: "Demon Slayer follows Tanjiro Kamado's journey to avenge his family and cure his sister.",
    trailer: "https://www.youtube.com/watch?v=VQGCKyvzIM4"
  },
  blackclover: {
    titleImg: "images/movies/black_title.png",
    year: "2017",
    rating: "13+",
    seasons: "4 Seasons",
    genres: "Action, Magic",
    description: "Black Clover follows Asta, a boy born without magic in a world where magic is everything.",
    trailer: "https://www.youtube.com/watch?v=PrgxJ1_sUkk"
  }
};

$(document).ready(function () {
  $('.carousel').carousel();

  $('.carousel-item').on('click', function () {
    const id = $(this).data('id');
    const anime = animeData[id];
    if (anime) {
      $('.movie-title').attr('src', anime.titleImg);
      $('.content h4').html(`
        <span>${anime.year}</span>
        <span><i>${anime.rating}</i></span>
        <span>${anime.seasons}</span>
        <span>${anime.genres}</span>
      `);
      $('.content p').text(anime.description);
      $('.button a:first').attr('href', anime.trailer);
      $('.carousel-trailer').attr('href', anime.trailer);
    }
  });
});