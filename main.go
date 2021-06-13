package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
)

func ptt(db *sql.DB, args []string) string {
	if len(args) <= 0 {
		return "Missing args."
	}

	if _, err := db.Exec("CREATE TABLE IF NOT EXISTS ptt (id text PRIMARY KEY)"); err != nil {
		return "Error creating database table: " + err.Error()
	}

	switch args[0] {
	case "list":
		rows, err := db.Query("SELECT id FROM ptt")
		if err != nil {
			return "Error reading ptt: " + err.Error()
		}

		var str string
		defer rows.Close()
		for rows.Next() {
			var id string
			if err := rows.Scan(&id); err != nil {
				return "Error scanning id: " + err.Error()
			}
			str += id + "\n"
		}
		return str
	case "add":
		if len(args) <= 1 {
			return "Missing args."
		}

		if _, err := db.Exec("INSERT INTO ptt VALUES ($1)", args[1]); err != nil {
			return "Error inserting id: " + err.Error()
		}
		return "Successfully added."
	case "remove":
		if len(args) <= 1 {
			return "Missing args."
		}

		if _, err := db.Exec("DELETE FROM ptt WHERE id = $1", args[1]); err != nil {
			return "Error deleting id: " + err.Error()
		}
		return "Successfully removed."
	default:
		return "Unknown Args."
	}
}

func main() {
	db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		log.Fatalf("Error opening database: %q", err)
	}

	bot, err := tgbotapi.NewBotAPI(os.Getenv("TOKEN"))
	if err != nil {
		log.Fatal(err)
	}

	bot.Debug = true

	log.Printf("Authorized on account %s", bot.Self.UserName)

	_, err = bot.SetWebhook(tgbotapi.NewWebhook("https://nevikw39-tg-bot.herokuapp.com/"))
	if err != nil {
		log.Fatal(err)
	}

	updates := bot.ListenForWebhook("/")
	go http.ListenAndServe("0.0.0.0:"+os.Getenv("PORT"), nil)

	for update := range updates {
		if update.Message == nil {
			continue
		}

		log.Printf("[%s] %s", update.Message.From.UserName, update.Message.Text)

		if update.Message.From.ID != 692286133 {
			msg := tgbotapi.NewMessage(update.Message.Chat.ID, "Sorry, you have no permission to access.")
			bot.Send(msg)
		}

		if update.Message.IsCommand() {
			msg := tgbotapi.NewMessage(update.Message.Chat.ID, "")
			switch update.Message.Command() {
			case "ptt":
				msg.Text = ptt(db, strings.Split(update.Message.CommandArguments(), " "))
			default:
				msg.Text = "Command not found."
			}
			bot.Send(msg)
		}
	}
}
