// *********************
// * NECESSARY HEADERS *
// *********************
#include <msp430.h> 
#include <string.h>
#include <stdlib.h>

// *****************
// * USEFUL MACROS *
// *****************
#define GREEN_LED                 BIT6
#define SAMPLE_RATE               50000

// Ultrasonic sensor constants
// ---------------------------
#define UltraPortOut              P2OUT
#define UltraPortDirection        P2DIR
#define UltraFrontPin             BIT1
#define UltraRightPin             BIT1
#define UltraEcho                 BIT0
#define SOUND_RATE                58
#define DISTANCE_THRESHOLD        20
#define timeToDistance(S, E)      (((E) - (S)) / SOUND_RATE)

// Current sensor constants
// ------------------------
#define CURRENT_THRESHOLD         1024
#define exponentialAverage(O, N)  (((O) >> 1) + ((O) >> 2) + ((N) >> 2))

// ***********************
// * FUNCTION PROTOTYPES *
// ***********************
void currentSetup(void);
void ultrasonicSetup(void);
void uartSetup(void);
void setup(void);
void serialPrint(const char *str);
void sampleDistance(void);
void sampleCurrents(void);

// *********************
// * NECESSARY GLOBALS *
// *********************
volatile unsigned int up = 0; // Helps the timer determine edge
volatile unsigned int startTime = 0;
volatile unsigned int endTime = 0;
volatile unsigned int currentMeasurements[8] = { 0 };
volatile unsigned int averagedCurrents[6] = { 0 };

// ********
// * MAIN *
// ********
int main(void) {
    setup();
    while(1) {
        _delay_cycles(SAMPLE_RATE);
		sampleCurrents();
        sampleDistance();
    }
}

// ********************
// * HELPER FUNCTIONS *
// ********************

// Setup
// -----
void currentSetup(void) {
    ADC10CTL1 = INCH_7 + CONSEQ_1; // A7-A0 single sequence
    ADC10CTL0 = ADC10SHT_2 + MSC + ADC10ON + ADC10IE;
    ADC10DTC1 = 8;   // 8 conversions
    ADC10AE0 = 0xF9; // skip A2/A1
}

void ultrasonicSetup(void) {
    // Timer1A capture configuration
    // -----------------------------
    // Rising/falling edge + synchronous + P2.0 (CCI1A) +
    // capture + capture/compare interrupt enable
    TA1CCTL0 |= CM_3 + CCIS_0 + CAP + CCIE;
    // SMCLK + make ta1ccr0 count continously up + no division
    TA1CTL |= TASSEL_2 + MC_2 + ID_0;
    // Set up pins for ultrasonic sensing
    // ----------------------------------
    UltraPortDirection = UltraFrontPin|UltraRightPin;
    // Turn off trigger pins to make sure they're in the correct state
    UltraPortOut &= ~(UltraFrontPin|UltraRightPin);
    // Set P2.0 to pick up echo from the HC-SR04
    // Not using a #define element for this - it's tied to the timer
    P2SEL = UltraEcho;
}

void uartSetup(void) {
	P1SEL = BIT1 + BIT2;                     // P1.1 = RXD, P1.2=TXD
    P1SEL2 = BIT1 + BIT2;                    // P1.1 = RXD, P1.2=TXD
    UCA0CTL1 |= UCSSEL_2;                    // SMCLK
    UCA0BR0 = 104;                           // 1MHz 9600
    UCA0BR1 = 0;                             // 1MHz 9600
    UCA0MCTL = UCBRS0;                       // Modulation UCBRSx = 1
    UCA0CTL1 &= ~UCSWRST;                    // Initialize USCI state machine
    IE2 |= UCA0RXIE;                         // Enable USCI_A0 RX interrupt
}

void setup(void) {
    WDTCTL = WDTPW + WDTHOLD;                // Stop WDT
    currentSetup();
    ultrasonicSetup();
    BCSCTL1 = CALBC1_1MHZ;                   // Set DCO
    DCOCTL = CALDCO_1MHZ;
	uartSetup();
    __bis_SR_register(GIE);  // Interrupts enabled
}

// UART communication
// ------------------
void serialPrint(const char *str) {
    static char pp = 0;
    while(pp);
    pp = 1;
    int i = 0;
    for(; str[i] != '\0'; i++) {
        while(!(IFG2 & UCA0TXIFG));
        UCA0TXBUF = str[i];
    }
    pp = 0;
}

// Current sensor
// --------------
void sampleCurrents(void) {
    ADC10CTL0 &= ~ENC;
    while(AD10CTL1 & BUSY);                        // Wait if ADC10 core active
    ADC10SA = (unsigned int) currentMeasurements;  // Copies data in ADC10SA
    ADC10CTL0 |= ENC + ADC10SC;                    // Start sampling

    averagedCurrents[0] =
        exponentialAverage(averagedCurrents[0], currentMeasurements[0]);
	
    averagedCurrents[1] =
        exponentialAverage(averagedCurrents[3], currentMeasurements[3]);
	
    averagedCurrents[2] =
        exponentialAverage(averagedCurrents[4], currentMeasurements[4]);
	
    averagedCurrents[3] =
        exponentialAverage(averagedCurrents[5], currentMeasurements[5]);
	
    averagedCurrents[4] =
        exponentialAverage(averagedCurrents[6], currentMeasurements[6]);
	
    averagedCurrents[5] =
        exponentialAverage(averagedCurrents[7], currentMeasurements[7]);

	int i = 0;
	for(; i < 6; i++) {
		if(averagedCurrents[i] > CURRENT_THRESHOLD) {
			serialPrint("s");
		}
	}
}

// Ultrasonic sensor
// -----------------
void sampleDistance(void) {
    UltraPortOut |= UltraFrontPin;
    // Next catch on Timer1A0 should be rising edge - helps with capture timer
    up = 1;
    UltraPortOut &= ~UltraFrontPin;
}

// **************
// * INTERRUPTS *
// **************
// Timer1_A Capture
// P2.0 ends up triggering this timer
// ----------------------------------
#pragma vector=TIMER1_A0_VECTOR
__interrupt void Timer1A0(void) {
    if(up) { // Rising edge
        startTime = TA1CCR0; // Start time of measurement
    } else { // Falling edge
        endTime = TA1CCR0;   // End time of measurement
        unsigned int distance = timeToDistance(startTime, endTime); // CM
        if(distance < DISTANCE_THRESHOLD) {
            // P1OUT |= GREEN_LED;
            serialPrint("b");
        } else {
            // P1OUT &= ~GREEN_LED;
			serialPrint("f");
        }
   }
   up = !up;         // Toggle edge
   TA1CTL &= ~TAIFG; // Clear timer A interrupt flag
}
