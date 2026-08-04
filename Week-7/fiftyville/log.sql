-- Keep a log of any SQL queries you execute as you solve the mystery.

-- The theft occurred on July 28, 2025 on Humphrey Street.
-- Find the crime scene report to gather the initial clues.
SELECT *
FROM crime_scene_reports
WHERE year = 2025
  AND month = 7
  AND day = 28
  AND street = 'Humphrey Street';

-- Read the interviews conducted on the day of the theft.
SELECT *
FROM interviews
WHERE year = 2025
  AND month = 7
  AND day = 28;

-- Based on Ruth's interview, the thief left the bakery parking lot
-- within 10 minutes after the theft. Find all cars that exited
-- between 10:15 AM and 10:25 AM.
SELECT *
FROM bakery_security_logs
WHERE year = 2025
  AND month = 7
  AND day = 28
  AND hour = 10
  AND minute BETWEEN 15 AND 25
  AND activity = 'exit';

-- Based on Eugene's interview, the thief withdrew money from the
-- Leggett Street ATM earlier that morning.
SELECT *
FROM atm_transactions
WHERE year = 2025
  AND month = 7
  AND day = 28
  AND atm_location = 'Leggett Street'
  AND transaction_type = 'withdraw';

-- Based on Raymond's interview, the thief made a phone call
-- lasting less than one minute after leaving the bakery.
SELECT *
FROM phone_calls
WHERE year = 2025
  AND month = 7
  AND day = 28
  AND duration < 60;

-- Raymond also mentioned that the thief planned to take the earliest
-- flight out of Fiftyville the next day. Find that flight.
SELECT *
FROM flights
WHERE year = 2025
  AND month = 7
  AND day = 29
ORDER BY hour, minute
LIMIT 1;

-- Find all passengers on the earliest flight (Flight 36).
SELECT
    p.name,
    p.phone_number,
    p.license_plate,
    p.passport_number
FROM people AS p
JOIN passengers AS pa
    ON p.passport_number = pa.passport_number
WHERE pa.flight_id = 36;

-- Combine all evidence:
-- 1. Left the bakery during the correct time.
-- 2. Withdrew money from the Leggett Street ATM.
-- 3. Made a phone call lasting less than one minute.
-- 4. Was a passenger on the earliest flight.
SELECT
    p.name,
    p.phone_number,
    p.license_plate,
    p.passport_number
FROM people AS p
JOIN bank_accounts AS b
    ON p.id = b.person_id
JOIN atm_transactions AS a
    ON b.account_number = a.account_number
WHERE p.license_plate IN
(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2025
      AND month = 7
      AND day = 28
      AND hour = 10
      AND minute BETWEEN 15 AND 25
      AND activity = 'exit'
)
AND a.year = 2025
AND a.month = 7
AND a.day = 28
AND a.atm_location = 'Leggett Street'
AND a.transaction_type = 'withdraw'
AND p.phone_number IN
(
    SELECT caller
    FROM phone_calls
    WHERE year = 2025
      AND month = 7
      AND day = 28
      AND duration < 60
)
AND p.passport_number IN
(
    SELECT passport_number
    FROM passengers
    WHERE flight_id = 36
);

-- The previous query identifies Bruce as the thief.
-- Find the accomplice by looking up the receiver of Bruce's phone call.
SELECT
    p.name
FROM people AS p
WHERE p.phone_number =
(
    SELECT receiver
    FROM phone_calls
    WHERE caller = '(367) 555-5533'
      AND year = 2025
      AND month = 7
      AND day = 28
      AND duration < 60
);

-- Find the destination city of the earliest flight.
SELECT city
FROM airports
WHERE id = 4;
