export default{
  data(){
      return{
        activeQuestion : null,
        services : ["Bathroom Repair;", "Ceiling Fan Repair;", "Countertop Repair;", "Deck Repair;","Door Repair;","Drywall Repair;", "Electrical Repair;"],
        choose : [
          {
            "title" : "Always Available",
            "description" : "We accept requests and phone calls 24/7 so you could resolve any problem whenever you need. Our emergency team will be at your place to fix the breakdown at short notice.",
            "icon" : "fa fa-clock"
          },
          {
            "title" : "Qualified Agents",
            "description" : "All our team members are high-qualified, educated and skilled agents. All of them are being trained according to the latest technologies. Our newbies work together with experienced colleagues to study all the details.",
            "icon" : "fa fa-star"
          },
          {
            "title" : "Fair Prices",
            "description" : "Our prices are both fair and affordable for all people. We offer flexible discount system so you could use any service you need.",
            "icon" : "fa fa-dollar-sign"
          },
          {
            "title" : "Best Offers",
            "description" : "We provide discounts on the most popular services and on the season services, so you could definitely receive any help without delay.",
            "icon" : "fa fa-star"
          }
        ],
        info : [
          {
            "title" : "Phone",
            "value" : "(719) 445-2808; (719) 445-2809;",
            "icon" : "fa fa-phone"
          },
          {
            "title" : "Address",
            "value" : "4578 Marmora Road, Glasgow",
            "icon" : "fa fa-map-marker"
          },
          {
            "title" : "E-mail",
            "value" : "info@demolink.org",
            "icon" : "fa fa-envelope"
          }
        ]
      }
  },
  methods: {
    getAnswer(index){
        this.activeQuestion = this.activeQuestion === index ? null : index;
      },
    getArrow(index){
        return this.activeQuestion === index ? "&#8595;" : '&#8594;';
    }
  }
}