package com.arl.data;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.text.DecimalFormat;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.Set;

/**
 *
 * @author rajendra
 */
public class GenerateDATA {

    private GenerateDATA() {
    }

    public static GenerateDATA getInstance() {
        return GenerateDATAHolder.INSTANCE;
    }

    private static class GenerateDATAHolder {

        private static final GenerateDATA INSTANCE = new GenerateDATA();
    }

    private String getCode(int k) {
        String ret = "";
        String str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/_*#^-";
        int count = 0;
        Random rand = new Random();

        do {
            int pos = Math.abs(rand.nextInt() % str.length());
            ret += str.charAt(pos);
            count++;
        } while (count < k);

        return ret;
    }
    private String getPNR(int k) {
        String ret = "";
        String str = "0123456789";
        int count = 0;
        Random rand = new Random();

        do {
            int pos = Math.abs(rand.nextInt() % str.length());
            ret += str.charAt(pos);
            count++;
        } while (count < k);

        return ret;
    }

    private String getDate() {
        String ret = "";
        Random rand = new Random();
        int d = 0, m = 0, y = 0;

        d = 1 + Math.abs(rand.nextInt() % 30);
        m = 1 + Math.abs(rand.nextInt() % 13);
        y = 1900 + Math.abs(rand.nextInt() % (2013 - 1900));

        ret = d + "/" + m + "/" + y;

        return ret;
    }

    private List<String> getCitiesList() {
        String cfile = System.getProperty("user.home") + "/resource/cities-u.txt";
        List<String> mylist = getList(cfile);
        System.out.println("City Names List Size: " + mylist.size());
        return mylist;
    }

    private List<String> getNamesList() {
        String cfile = System.getProperty("user.home") + "/resource/malefemalenames.txt";
        List<String> mylist = getList(cfile);
        System.out.println("Stock Traders List Size: " + mylist.size());
        return mylist;
    }

    private List<String> getCameraList() {
        String cfile = System.getProperty("user.home") + "/resource/cameralist.txt";
        List<String> mylist = getList(cfile);
        System.out.println("Camera List Size: " + mylist.size());
        return mylist;
    }

    private List<String> getPassengerList() {
        String cfile = System.getProperty("user.home") + "/resource/passengernames.txt";
        List<String> mylist = getList(cfile);
        System.out.println("Passenger List Size: " + mylist.size());
        return mylist;
    }

    private List<String> getBusNameList() {
//        String cfile = System.getProperty("user.home") + "/Data/resource/busnames.txt";
        String cfile = "busnames.txt";
        List<String> mylist = getList(cfile);
        System.out.println("Bus Names List Size: " + mylist.size());
        return mylist;
    }

    private List<String> getList(String cfile) {
        Set<String> ucset = new HashSet<String>();
        List<String> listhash = new LinkedList<>();
        try {
            BufferedReader br = new BufferedReader(new FileReader(cfile));
            String line;
            while ((line = br.readLine()) != null) {
                ucset.add(line);
            }
            listhash.addAll(ucset);
        } catch (IOException Ex) {
            System.err.println("ERROR: Unable to get the List!!");
        }
        return listhash;
    }

    public void GenerateStockTradeDataset(String file, int count) {
        try {
            List<String> namehash = getNamesList();
            Random rand = new Random(System.nanoTime());
            Random rnum = new Random(System.nanoTime());
            File cfile = new File(file);
            System.out.flush();
            try (OutputStream output = new FileOutputStream(file); PrintStream print = new PrintStream(output)) {
                System.setOut(print);
                System.out.println("Name    Age   Transaction-Date  Buying-Stock   Buying-Code  Buying-Cost  Selling-Stock   Selling-Code   Selling-Cost   Amount");
                for (int i = 0; i < count; i++) {
                    int pos = Math.abs(rand.nextInt()) % 1024;

                    String trasdate = getDate();
                    String name = namehash.get(pos);

                    int sbuy = 100 + Math.abs(rand.nextInt()) % (1000 - 100);
                    String bcode = getCode(8);
                    float bcost = 1000 + Math.abs(rand.nextInt()) % (10000 - 1000);

                    int ssell = 100 + Math.abs(rand.nextInt()) % (1000 - 100);
                    String scode = getCode(8);
                    float scost = 1000 + Math.abs(rand.nextInt()) % (10000 - 1000);

                    int amount = (int) scost - (int) bcost;

                    System.out.println(name + " " + trasdate + " " + sbuy + " " + bcode + " " + bcost + " " + ssell + " " + scode + " " + scost + " " + amount);
                }
            }
            System.out.flush();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void GenerateCameraDataset(String file, int count) {
        try {
            List<String> namehash = getCameraList();
            Random rand = new Random(System.nanoTime());
            Random rnum = new Random(System.nanoTime());
            File cfile = new File(file);

            System.out.flush();
            try (OutputStream output = new FileOutputStream(file); PrintStream print = new PrintStream(output)) {
                DecimalFormat df2 = new DecimalFormat("#.##");
                System.setOut(print);
                System.out.println("Bill-Code    Camera-Name   Transaction-Date  Type   Brand  Rating  MRP   Discount   Delivery-Changes   Final-Cost");
                for (int i = 0; i < count; i++) {
                    String trasdate = getDate();

                    int pos = Math.abs(rand.nextInt()) % namehash.size();
                    String camera = namehash.get(pos);

                    String billcode = getCode(8);
                    double mrp = 1000.0 + (Math.abs(rand.nextInt()) % (40000.0 - 1000.0)) + Math.abs(rand.nextDouble()) % 10.0;

                    int ptype = Math.abs(rand.nextInt()) % 3;

                    String pbrand = camera.split("\\s+")[0].trim();
                    double rate = Math.abs(rand.nextDouble()) % 10.0;
                    double discount = 1.0 + (Math.abs(rand.nextInt()) % (100.0 - 34.0)) + Math.abs(rand.nextDouble()) % 10.0;
                    double charges = 50.0 + (Math.abs(rand.nextInt()) % (300.0 - 50.0)) + Math.abs(rand.nextDouble()) % 10.0;

                    double cost = Math.abs(mrp - (mrp * (discount / 100)) + charges);

                    System.out.println(billcode + "," + camera + "," + trasdate + "," + ptype + "," + pbrand + "," + df2.format(rate) + "," + df2.format(mrp) + "," + df2.format(discount) + "," + df2.format(charges) + "," + df2.format(cost));
                }
            }
            System.out.flush();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void GenerateBusBookingsDataset(String file, int count) {
        try {
            List<String> namehash = getPassengerList();
            Random rand = new Random(System.nanoTime());
            Random rnum = new Random(System.nanoTime());
            File cfile = new File(file);

            System.out.flush();
            try (OutputStream output = new FileOutputStream(file); PrintStream print = new PrintStream(output)) {
                DecimalFormat df2 = new DecimalFormat("#.##");
                System.setOut(print);

                System.out.println("Tick ID | Bus Name           | Date     | Quota | Passenger Name       | Age | Seat | Code | TYPE | FARE ");
                for (int i = 0; i < count; i++) {
                    String ticketID = getCode(11);

                    String bnames[] = { "Speed Beast", "Fast Charminar", "Flying Wings", "Hyper Points", "Silk Express",
                        "Steel Rider", "Luxury Ride", "Moving Heaven", "State Flyer", "Ambassdor Cage", "Hybrid Pearl", "Sea Stone" };
                    String bcodes[] = { "SPE", "FCB", "FWS", "HPS", "SEB", "SRS", "LRE", "MHC", "SFC", "ACE", "HPS", "SSC" };

                    int ppos = Math.abs(rnum.nextInt()) % bcodes.length;
                    String busname = bnames[ppos];


                    String traveldate = getDate();
                    int quota = Math.abs(rand.nextInt()) % 5;

                    int pos = Math.abs(rand.nextInt()) % namehash.size();
                    String passname = namehash.get(pos);

                    int age = 1 + Math.abs(rnum.nextInt() % (100 - 1));
                    int seat = 1 + Math.abs(rnum.nextInt() % (56 - 1));
                    String buscode = bcodes[ppos];
                    int type = Math.abs(rand.nextInt()) % 4;

                    double fare = 100.0 + (Math.abs(rand.nextInt()) % (2000.0 - 100.0)) + Math.abs(rand.nextDouble()) % 10.0;

                    System.out.println(ticketID + "," + busname + "," + traveldate + "," + quota + "," + passname + "," + age + ","
                            + seat + "," + buscode + "," + type + "," + df2.format(fare));
                }
            }
            System.out.flush();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void GenerateTrainBookingsDataset(String file, int count) {
        try {
            List<String> namehash = getPassengerList();
            Random rand = new Random(System.nanoTime());
            Random rnum = new Random(System.nanoTime());
            File cfile = new File(file);

            System.out.flush();
            try (OutputStream output = new FileOutputStream(file); PrintStream print = new PrintStream(output)) {
                DecimalFormat df2 = new DecimalFormat("#.##");
                System.setOut(print);

                System.out.println("PNR | Train Name           | Date     | Quota | Passenger Name       | Age | Seat | Code | TYPE | FARE ");
                for (int i = 0; i < count; i++) {
                    String PNR = getPNR(11);

                    String trainnames[] = { "HOWRAH EXPRESS", "JNANESWARI DELX", "BKSC HWH PAS", "CKP HWH PAS", "HOWRAH MAIL", "AZAD HIND EXP",
                        "PURI HWH EXPRESS", "KORAPUT HWH EXP", "HOWRAH MAIL", "YPR HOWRAH EXP", "KRIYA YOGA EXP", "PURI HWH G RATH",
                        "SRIJAGANNATH EXP", "VSKP SHM SF EXP", "BHUJ SHM EXP", "STEEL EXP", "PRR HWH EXP", "LTT SHALIMAR EX", "COROMANDEL EXP",
                        "GITANJALI EXP", "BBS JAN SHATABDI", "HOWRAH EXPRESS", "GUWAHATI EXP", "SATABDI EXPRESS", "RNC HWH INT EXP",
                        "EAST COAST EXP", "YPR HWH AC EXP", "FALAKNUMA EXP", "MAS SRC EXPRESS", "ISPAT EXPRESS", "ARANYAK EXPRESS", "DHAULI EXP",
                        "BBN JANSHATABDI", "RUPASIBANGLA EXP", "KARMABHOOMI EXP", "PDY HOWRAH EXP", "JP SHM SPL" };

                    int ppos = Math.abs(rnum.nextInt()) % trainnames.length;
                    String trainname = trainnames[ppos];

                    String traveldate = getDate();
                    int quota = Math.abs(rand.nextInt()) % 5;

                    int pos = Math.abs(rand.nextInt()) % namehash.size();
                    String passname = namehash.get(pos);

                    int age = 1 + Math.abs(rnum.nextInt() % (100 - 1));
                    int seat = 1 + Math.abs(rnum.nextInt() % (56 - 1));

                    String couches[] = { "FA1", "SA1", "SA3", "S1", "S2", "S3",  "S4",  "S5",  "S6",  "S7",  "S8",  "S9",  "S10",  "S11", "S12",  "G1",  "G2",  "G3" };

                    int cpos = Math.abs(rnum.nextInt()) % couches.length;
                    String coachID = couches[cpos];

                    int type = Math.abs(rand.nextInt()) % 4;

                    double fare = 100.0 + (Math.abs(rand.nextInt()) % (2000.0 - 100.0)) + Math.abs(rand.nextDouble()) % 10.0;

                    System.out.println(PNR + "," + trainname + "," + traveldate + "," + quota + "," + passname + "," + age + ","
                            + seat + "," + coachID + "," + type + "," + df2.format(fare));
                }
            }
            System.out.flush();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void GenerateWeatherDataset(String file, int count) {
        try {
            Random rand = new Random(System.nanoTime());
            List<String> citynames = getCitiesList();
            File cfile = new File(file);
            System.out.flush();
            try (OutputStream output = new FileOutputStream(file); PrintStream print = new PrintStream(output)) {
                System.setOut(print);

                System.out.print("City, Date, Temp-Low, Temp-High");

                for (int i = 0; i < count; i++) {
                    String text;
                    int pos = Math.abs(rand.nextInt()) % 25;
                    String city = citynames.get(pos);

                    String date = getDate();

                    double min = (rand.nextDouble() * 100) % 50.0f;
                    double max = (rand.nextDouble() * 100) % 50.0f;
                    if (max < min) {
                        max = max + min;
                        min = max - min;
                        max = max - min;
                    }
                    System.out.format("%s,%s,%8.6f,%8.6f\n", city, date, min, max);
                }
            }
            System.out.flush();
        } catch (Exception e) {
        }
    }

    public void showUsage() {
        System.out.println("USAGE: java -cp " + System.getProperty("user.dir") + "/GenerateData.jar " + this.getClass().getName()
                + " [-d target Directory] [-f output file name] [-n number of records] [-s dataset acronym]");
        System.exit(0);
    }

    public static void main(String[] args) {
        GenerateDATA gd = GenerateDATA.getInstance();

        /* If arguments are insufficient, then throw the error message */
        if (args.length < 1) {
            gd.showUsage();
        }

        String cfile = "", targetDir = "", datasetname = "";
        int nrecos = 10000;
        for (int i = 0; i < args.length; i++) {
            if ("-d".equalsIgnoreCase(args[i])) {
                targetDir = args[i + 1];
                i++;
            }

            if ("-f".equalsIgnoreCase(args[i])) {
                cfile = args[i + 1];
                i++;
            }

            if ("-s".equalsIgnoreCase(args[i])) {
                datasetname = args[i + 1];
                i++;
            }

            if ("-n".equalsIgnoreCase(args[i])) {
                nrecos = Integer.parseInt(args[i + 1]);
                i++;
            }
        }

        cfile = (targetDir.isEmpty()) ? System.getProperty("user.dir") + "/" + cfile : targetDir + "/" + cfile;
        boolean add = new File(cfile).getParentFile().mkdirs();

        if (datasetname.equalsIgnoreCase("camera")) {
            gd.GenerateCameraDataset(cfile, nrecos);
        } else if (datasetname.equalsIgnoreCase("stock")) {
            gd.GenerateStockTradeDataset(cfile, nrecos);
        } else if (datasetname.equalsIgnoreCase("weather")) {
            gd.GenerateWeatherDataset(cfile, nrecos);
        } else if (datasetname.equalsIgnoreCase("bus")) {
            gd.GenerateBusBookingsDataset(cfile, nrecos);
        } else if (datasetname.equalsIgnoreCase("train")) {
            gd.GenerateTrainBookingsDataset(cfile, nrecos);
        } else {
            gd.GenerateStockTradeDataset(cfile, nrecos);
        }

        System.out.println("\nDataset: " + cfile + " created successfully!\n");

        System.out.println("Done!!");
    }

}
